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

    return app
