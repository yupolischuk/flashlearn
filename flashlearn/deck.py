from flask import Blueprint
from flask import render_template
from flask import request

from flashlearn.db import connect

bp = Blueprint('deck', __name__)

engine = connect()


@bp.route('/deck/')
def index():

    return render_template('deck.html')