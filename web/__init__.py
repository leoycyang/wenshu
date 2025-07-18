from flask import Flask

from .db import DB

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
    app.guiding_cases = app.db.execute(f'SELECT {", ".join(app.guiding_case_columns)} FROM guiding_cases')

    return app
