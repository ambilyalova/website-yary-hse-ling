from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from db_models import User
def register_routes(app, db, bcrypt):
    @app.route('/')
    def index():
        return render_template('main_page.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'GET':
            return render_template('register.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

            hashed_password = bcrypt.generate_password_hash(password)

            user = User(username=username, email=email, password=hashed_password)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('index'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter(username=username).first()

            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                return 'Login Failed'
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))
