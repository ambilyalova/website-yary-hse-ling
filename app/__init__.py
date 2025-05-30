from flask_bcrypt import Bcrypt
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate, migrate
from app.auth.routes import auth
from app.flashcards.routes import flashcards
from app.db_models import db, User
from app.profile.routes import profile
from app.test_mode.routes import test_mode


def create_app():
    app = Flask(__name__, template_folder='templates')

    username = "adeliysw_yaryhse"
    password = "rqOIpW4SagXh"
    db_name = "adeliysw_yaryhse"

    app.config[
        'SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://" + username + ":" + password + "@adeliysw.beget.tech/" + db_name + "?charset=utf8"
    app.config['SECRET_KEY'] = 'iI8eVtfdzioDG7b'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    def inject_user():
        return dict(current_user=current_user)

    bcrypt = Bcrypt(app)

    migrate = Migrate(app, db)

    from app.auth.routes import register_routes
    register_routes(db, bcrypt)

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(flashcards, url_prefix='/flashcards')

    from app.profile.routes import register_routes
    register_routes()

    app.register_blueprint(profile, url_prefix='/profile')

    app.register_blueprint(test_mode, url_prefix='/test_mode')

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
