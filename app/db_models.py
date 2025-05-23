from datetime import date
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    total_score = db.Column(db.Integer, default=0)
    tests_taken = db.Column(db.Integer, default=0)

    test_results = db.relationship('TestResult', backref='users', lazy=True)

    def get_id(self):
        return self.id

    def get_average_score(self):
        if self.tests_taken == 0:
            return 0
        return self.total_score / self.tests_taken

    def __repr__(self):
        return f"<User {self.username}, email={self.email}>"


class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, default=date.today)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
