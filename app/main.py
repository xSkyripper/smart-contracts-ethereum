import os
from flask import (
    Blueprint,
    render_template,
    current_app,
    send_file,
    )

from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
    )

main_bp = Blueprint('main_bp', __name__,
                    url_prefix='',
                    static_url_path='',
                    static_folder='./dist/static/',
                    template_folder='./dist/',
                    )

@main_bp.route('/')
def index_client():
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    pass

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    pass

@main_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    pass


