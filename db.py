from dataclasses import dataclass
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


username = "x91654hf_hselang"
password = "*TEo4@jQC9ho"
db_name = "x91654hf_hselang"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://" + username + ":" + password + "@localhost/" + db_name + "?charset=utf8"
db = SQLAlchemy()
db.init_app(app)

if __name__ == "__main__":
    app.run()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)


    def __repr__(self):
        return f"<User {self.username}, email={self.email}>"
