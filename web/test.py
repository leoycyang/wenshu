from flask import current_app as app
from flask import request, render_template, jsonify

from flask import Blueprint
bp = Blueprint('test', __name__)

@bp.route('/')
def hello():
    return 'Hello, World!'
