import os

from flask import Flask
from app.shared import db

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = "sqlite:///{}".format(os.path.join(PROJECT_DIR, "database.db"))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_FILE
db.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# Register route
# Login route
# get Contracts

# Users C R U D
# Contracts C R U D
# Contracts-Users

if __name__ == '__main__':
    app.run()