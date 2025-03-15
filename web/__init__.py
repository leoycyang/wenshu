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
    from .test import bp as test_bp
    app.register_blueprint(test_bp)

    return app
