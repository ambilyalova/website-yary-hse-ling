from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from datetime import date
from pathlib import Path
import json
import random

test_mode = Blueprint('test_mode', __name__, template_folder='templates')

# грузит языки с json
def load_languages():
    current_dir = Path(__file__).parent
    data_path = 'app/data/languages_classification.json'
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# генерирует рандомный язык для теста по счетчику
def get_random_languages(count=10):
    languages = load_languages()
    return random.sample(languages, count)

# нижний регистр без ё для всех ответов
def normalize_answer(answer):
    return answer.lower().strip().replace("ё", "е") if answer else ""

# стартовая страница с инструкцией
@test_mode.route('/start')
def home():
    return render_template('start.html')

# генерит 10 языков и начинает сессии для языков и ответов пользователя
@test_mode.route('/start_test')
def start_test():
    session.clear()
    test_languages = get_random_languages(10)
    session['test_languages'] = test_languages
    session['current_language'] = 0
    session['user_answers'] = {}
    return redirect(url_for('test_mode.show_question'))

# работа с вопросами
@test_mode.route('/question')
def show_question():
    
    # навигация по вопросам
    if 'move_to' in request.args:
        new_idx = int(request.args['move_to'])
        if 0 <= new_idx < len(session.get('test_languages', [])):
            session['current_language'] = new_idx

    current_idx = session.get('current_language', 0)
    test_languages = session.get('test_languages', [])

    # переход к странице с результатами (если надо)
    if current_idx >= len(test_languages):
        return redirect(url_for('test_mode.show_results'))

    # подгружает ответы пользователя из сессии (если ещё не результаты)
    user_answers = session.get('user_answers', {})
    saved_answers = user_answers.get(str(current_idx), {})

    # переход к странице с вопросом
    return render_template('question.html',
                           lang_num=current_idx + 1,
                           lang_name=test_languages[current_idx]['name'],
                           total_langs=len(test_languages),
                           saved_answers=saved_answers,
                           all_languages=test_languages)

# перезаписывает ответы в нормализованном виде
@test_mode.route('/save_answer', methods=['POST'])
def save_answer():
    current_idx = session.get('current_language', 0)
    user_answers = session.get('user_answers', {})

    user_answers[str(current_idx)] = {
        'macrofamily': normalize_answer(request.form.get('macrofamily')),
        'family': normalize_answer(request.form.get('family')),
        'branch': normalize_answer(request.form.get('branch')),
        'group': normalize_answer(request.form.get('group'))
    }

    session['user_answers'] = user_answers

    #это для AJAX-запроса
    return jsonify({'status': 'success'})

# сохраняет ответ на последний вопрос перед результатами
@test_mode.route('/final_submit', methods=['POST'])
def final_submit():
    save_answer()  
    return redirect(url_for('test_mode.show_results'))

# обработка результатов
@test_mode.route('/results')
def show_results():
    test_languages = session.get('test_languages', [])
    user_answers = session.get('user_answers', {})

    results = []
    total_score = 0

    # начинает проверять каждый язык по очереди
    for idx, lang_data in enumerate(test_languages):
        user_answer = user_answers.get(str(idx), {})
        correct_answer = lang_data.get('classification', {})

        # проверяет каждое поле
        all_correct = True
        for field in ['macrofamily', 'family', 'branch', 'group']:
            user_val = normalize_answer(user_answer.get(field, ''))
            correct_val = normalize_answer(correct_answer.get(field, ''))
            if user_val != correct_val:
                all_correct = False
                break
                
        # засчитывает балл, если все поля верные
        lang_score = 1 if all_correct else 0
        total_score += lang_score

        # добавляет информацию в результаты
        results.append({
            'lang_name': lang_data['name'],
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': all_correct,
            'lang_score': lang_score
        })

    # переход на страницу с результатами
    return render_template('results.html',
                           results=results,
                           total_score=total_score,
                           max_score=10)

