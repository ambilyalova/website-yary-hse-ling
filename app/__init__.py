from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)

    username = "x91654hf_hselang"
    password = "*TEo4@jQC9ho"
    db_name = "x91654hf_hselang"

    app.config[
        'SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://" + username + ":" + password + "@localhost/" + db_name + "?charset=utf8"
    db = SQLAlchemy()
    db.init_app(app)

    return app
