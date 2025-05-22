from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash
import re

app = Flask(__name__)

# Конфигурация MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'genealogy_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql = MySQL(app)


@app.route('/')
def index():
    return redirect(url_for('register'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Получаем данные из формы
        username = request.form.get['username']
        email = request.form.get['email']
        password = request.form.get['password']

        # Валидация данных
        if not username or not email or not password:
            flash('Все поля должны быть заполнены!', 'danger')
            return redirect(url_for('register'))

        if len(password) < 6:
            flash('Пароль должен содержать не менее 6 символов', 'danger')
            return redirect(url_for('register'))

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Некорректный email адрес', 'danger')
            return redirect(url_for('register'))

        # Проверка, существует ли пользователь
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()

        if user:
            flash('Пользователь с таким email уже существует', 'danger')
            return redirect(url_for('register'))

        # Добавление пользователя в базу данных с хешированным паролем
        try:
            hashed_password = generate_password_hash(password)
            cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                        (username, email, hashed_password))
            mysql.connection.commit()
            cur.close()
            flash('Регистрация прошла успешно!', 'success')
            return redirect(url_for('register'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Ошибка при регистрации: {str(e)}', 'danger')
            return redirect(url_for('register'))

    # GET запрос - отображаем форму регистрации
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)