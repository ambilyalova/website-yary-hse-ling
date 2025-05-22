from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)

# Конфигурация MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'genealogy_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Секретный ключ для сессий
app.secret_key = 'your_secret_key_here'

mysql = MySQL(app)


@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
    # (Существующий код регистрации без изменений)
    # ...

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Получаем данные из формы
        username_or_email = request.form['username']
        password = request.form['password']

        # Проверяем заполненность полей
        if not username_or_email or not password:
            flash('Все поля должны быть заполнены!', 'danger')
            return redirect(url_for('login'))

        # Ищем пользователя в базе данных
        cur = mysql.connection.cursor()

        # Проверяем, является ли ввод email или username
        if '@' in username_or_email:
            cur.execute("SELECT * FROM users WHERE email = %s", (username_or_email,))
        else:
            cur.execute("SELECT * FROM users WHERE username = %s", (username_or_email,))

        user = cur.fetchone()
        cur.close()

        if user:
            # Проверяем пароль
            if check_password_hash(user['password'], password):
                # Успешная авторизация
                session['logged_in'] = True
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash('Вы успешно вошли в систему!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Неверный пароль', 'danger')
        else:
            flash('Пользователь с такими данными не найден', 'danger')

        return redirect(url_for('login'))

    # GET запрос - отображаем форму входа
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session or not session['logged_in']:
        flash('Пожалуйста, войдите в систему', 'warning')
        return redirect(url_for('login'))

    return f"Добро пожаловать, {session['username']}! Это ваша личная страница."


@app.route('/logout')
def logout():
    session.clear()
    flash('Вы успешно вышли из системы', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)