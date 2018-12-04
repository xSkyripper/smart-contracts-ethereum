import os
from flask import Blueprint, render_template, current_app

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


