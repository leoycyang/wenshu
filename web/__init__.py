from flask import Flask

from .db import DB
import datetime

def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE='wenshu.db',
    )

    app.db = DB(app)
    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    app.guiding_case_columns = ['id', 'case_title', 'series', 'guiding_case_number', 'publication_date' ]
    app.guiding_cases = []
    for row in app.db.execute(f'SELECT {", ".join(app.guiding_case_columns)} FROM guiding_cases'):
        case = {}
        for i, column in enumerate(app.guiding_case_columns):
            case[column] = row[i]
            if column == 'publication_date':
                case[column] = datetime.datetime.strptime(case[column], '%Y-%m-%d')
        app.guiding_cases.append(case)

    return app
