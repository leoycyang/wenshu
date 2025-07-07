import re

from flask import current_app as app
from flask import request, render_template, jsonify

from flask import Blueprint
bp = Blueprint('test', __name__)

@bp.route('/')
def hello():
    return render_template('index.html')

@bp.route("/contents", methods=['GET'])
def contents():
    fulltext_pattern = request.args.get('query')
    if fulltext_pattern is None:
        fulltext_pattern = ''
    rows = app.db.execute('select case_id, case_title, full_text from wenshu where full_text REGEXP :pattern LIMIT 1000',
                          pattern=fulltext_pattern)
    data = []
    for caseid, casetitle, fulltext in rows:
        data.append({"ID": caseid, "Name": casetitle, "Text": fulltext})
    return jsonify(data)

@bp.route('/shit/<int:num_shit>')
def shit(num_shit):
    return f'{num_shit} shits pooped today'

@bp.route('/case/<int:rowid>')
def case(rowid):
    output_items = list()
    rows = app.db.execute(f'select rowid, full_text from wenshu where rowid={rowid}')
    for this_rowid, this_full_text in rows:
        output_items.append(str(this_rowid))
        output_items.append(str(this_full_text))
        refs = extract_refs(this_full_text)
        output_items.append(','.join(refs))
    return '<pre>' + '\n'.join(output_items) + '</pre>'

def extract_refs(full_text):
    extract = list()
    title_match = re.search('《([^》]*)》.{0,50}指导.{0,10}案例', full_text)
    if title_match is not None:
        # print(title_match.group(0))
        extract.append(str(title_match.group(1)))
    return extract