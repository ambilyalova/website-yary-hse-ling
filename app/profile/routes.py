from flask import render_template, request, redirect, url_for, Blueprint
from flask_login import current_user
from app.db_models import User, TestResult, db

profile = Blueprint('profile', __name__, template_folder='templates')

def register_routes():
    @profile.route('/')
    def profile_page():
        username = current_user.username
        email = current_user.email
        data = db.session.query(TestResult.date, TestResult.score)\
    .filter(TestResult.user_id == current_user.id)\
    .order_by(TestResult.date.desc())\
    .limit(10)\
    .all()

        results = []
        for date, score in data:
            if date and score is not None:  # Filter out None values
                results.append([
                    date.strftime('%Y-%m-%d'),  # Convert date to string
                    int(score)  # Ensure score is integer
                ])
        results.reverse()
        average = round(current_user.total_score / current_user.tests_taken, 2)
        return render_template('profile.html', username=username, email=email, result=results, average=average)