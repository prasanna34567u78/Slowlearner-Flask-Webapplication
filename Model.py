from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

app = Flask(__name__)
app.secret_key = 'heiuhin3vu094890nncjiiuhvjjvbvijbv'


login_manager = LoginManager(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['slowlearners']
students_collection = db['students']

# Load the pre-trained Random Forest model
rf_model = joblib.load('RandomForest.joblib')

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(usn):
    student = students_collection.find_one({'USN': usn})
    if student:
        user = User()
        user.id = usn
        return user
    return None



@app.route('/')
def index():
    return render_template('login.html')

@app.route('/student')

def student():
    return render_template('student.html')

@app.route('/teacher')
@login_required
def teacher():
    return render_template('teacher.html')

@app.route('/about')
@login_required
def about():
    usn = current_user.id
    student = students_collection.find_one({'USN': usn})
    return render_template('about.html',student=student)

@app.route('/profile')
@login_required
def profile():
    usn = current_user.id
    student = students_collection.find_one({'USN': usn})
    return render_template('profile.html',student=student)

@app.route('/contact')
@login_required
def contact():
    usn = current_user.id
    student = students_collection.find_one({'USN': usn})
    return render_template('contact.html',student=student)


@app.route('/login', methods=['POST'])
def login():
    usn = request.form.get('usn')
    password = request.form.get('password')

    student = students_collection.find_one({'USN': usn, 'password': password})
    print("st",student)
    if student:
        user = User()
        user.id = usn
        login_user(user)
        return redirect(url_for('home'))

    return 'Login Failed'

    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


def calculate_cie(row):
    ia_scores = [row['IA1'], row['IA2'], row['IA3']]
    best_two = sorted(ia_scores, reverse=True)[:2]
    sum_ = sum(best_two) + row['CTA']
    return sum_

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    usn = current_user.id
    student = students_collection.find_one({'USN': usn})
    return render_template('home.html', student=student)




if __name__ == '__main__':
    app.run(debug=True)
