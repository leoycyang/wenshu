import datetime

from flask import current_app as app
from flask import request, render_template, jsonify

from flask import Blueprint
bp = Blueprint('main', __name__)

from . import guiding

@bp.route('/hello')
def hello():
    return 'Hello, World!'

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

@bp.route('/api/extract-guiding', methods=['POST'])
def extract_guiding():
    rowid = request.get_json()['rowid']
    full_text = app.db.execute(f'SELECT full_text FROM wenshu WHERE rowid = :rowid', rowid=rowid)[0][0]
    results = guiding.extract(full_text, r'(?P<anchor>指导.{0,5}案例)', r'.{100}$', r'^.{100}', [
        r'(?P<case_number>\d+)号案', 
        r'(?P<number>\d+)号(?!案)',
        r'《(?P<case_title>[^》]*)》', r'“(?P<case_title>[^”]+)”', 
        r'(?<!\d)(?P<year>\d{4})(?!\d)',
        r'(?P<month>\d{1,2})月',
        r'［(?P<case_pub_ref>[^］]*)］',
        r'(?P<series>\d+)[批|期|辑]',
    ])
    guilding_titles = [c[app.guiding_case_columns.index('case_title')] for c in app.guiding_cases]
    for result in results:
        for extract in result['extracts']:
            if extract['label'] == 'case_title':
                case_title = extract['text']
                guiding_index, score = guiding.simrank(case_title, guilding_titles, 1)[0]
                extract['text'] += f' -> {app.guiding_cases[guiding_index][app.guiding_case_columns.index('guiding_case_number')]} (score: {score})'
    return jsonify(dict(results=results, full_text=full_text))

@bp.route('/')
def index():
    return render_template(
        'listing.html'
    )

@bp.route('/case/', defaults={'rowid': None})
@bp.route('/case/<int:rowid>')
def case_detail(rowid):
    case_id, full_text = app.db.execute(f'SELECT case_id, full_text FROM wenshu WHERE rowid = :rowid', rowid=rowid)[0]
    return render_template(
        'case.html',
        rowid = rowid,
        case_id = case_id,
        full_text = full_text,
    )
