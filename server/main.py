import os
import sys
from flask import Flask, request, render_template, redirect
from app.models import *
from app.repo import UserRepository

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = "sqlite:///{}".format(os.path.join(PROJECT_DIR, "database.db"))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_FILE
db.init_app(app)
app.app_context().push()

user_repository = UserRepository()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users', methods=['GET'])
def get_users():
    users = user_repository.get_users()
    return render_template('users.html', users=users)

@app.route('/users', methods=['POST'])
def post_users():
    new_user = User(gov_id=request.form['gov_id'],
                    first_name=request.form['first_name'],
                    last_name=request.form['last_name'],
                    ethereum_id=request.form['gov_id'][::-1])
    user_repository.add_user(new_user)
    return redirect('/users')

# Register route
# Login route
# Get Contracts

# Users C R U D
# Contracts C R U D
# Contracts-Users

if __name__ == '__main__':
    answer = input("Create database?(Y/N)")
    if answer == "Y":
        db.create_all()
    app.run(debug=True)