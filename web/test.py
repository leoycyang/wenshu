from flask import current_app as app
from flask import request, render_template, jsonify

from flask import Blueprint
bp = Blueprint('test', __name__)

@bp.route('/')
def hello():
    return 'Hello, World!'

@bp.route('/test')
def test():
    lines = list()
    for rowid, _, _, full_text in app.db.execute('''
SELECT rowid, case_id, case_title, full_text
FROM wenshu
WHERE full_text REGEXP :pattern
LIMIT :limit OFFSET 0
''', pattern='指导.{0,10}案例', limit=5):
        lines.append(f'{rowid}: {full_text}')
    return '\n\n'.join(lines)
