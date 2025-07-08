import datetime
import re

from flask import current_app as app
from flask import request, render_template, jsonify

from flask import Blueprint
bp = Blueprint('main', __name__)

def str_to_val(argtype, arg):
    if argtype == 'DATE':
        return datetime.datetime.strptime(arg, '%Y-%m-%d').date()
    elif argtype == 'TEXT':
        return arg
    else:
        return arg # ideally, we should infer a precise type, but keeping numbers as strings works for sqlalchemy

def json_to_sql(args):
    conds = list()
    bindings = dict()
    for key, value in args.items():
        if key in ('offset', 'limit'):
            bindings[key] = int(value)
        elif value['type'] == 'NUMERIC' or value['type'] == 'DATE':
            if value['operator'] == 'EQUAL_TO':
                conds.append(f'{key} = :{key}')
                bindings[key] = str_to_val(value['type'], value['input'])
            elif value['operator'] == 'BETWEEN':
                conds.append(f'{key} BETWEEN :_{key}_1 AND :_{key}_2')
                bindings[f'_{key}_1'] = str_to_val(value['type'], value['input'])
                bindings[f'_{key}_2'] = str_to_val(value['type'], value['input2'])
        elif value['type'] == 'TEXT':
            conds.append(f'{key} REGEXP :{key}')
            bindings[key] = str_to_val(value['type'], value['input'])
    sql = '' if len(conds) == 0 else ' WHERE ' + ' AND '.join(conds)
    sql += ' ORDER BY rowid'
    if 'limit' in bindings:
        sql += ' LIMIT :limit'
    if 'offset' in bindings:
        sql += ' OFFSET :offset'
    return sql, bindings

@bp.route('/api/summarize', methods=['POST'])
def summarize():
    sql, bindings = json_to_sql(request.get_json())
    return jsonify({
        'column_names': ['rowid'] + app.db.column_names('wenshu'),
        'row_count': app.db.execute(f'SELECT COUNT(*) FROM wenshu{sql}', **bindings)[0][0]
    })

@bp.route('/api/fetch', methods=['POST'])
def fetch():
    sql, bindings = json_to_sql(request.get_json())
    rows = app.db.execute(f'SELECT rowid, * FROM wenshu{sql}', **bindings)
    return jsonify({
        'rows': [[col for col in row] for row in rows]
    })

@bp.route('/')
def index():
    return render_template(
        'listing.html'
    )

@bp.route('/case/', defaults={'rowid': None})
@bp.route('/case/<int:rowid>')
def case_detail(rowid):
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