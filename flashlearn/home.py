from flask import Blueprint
from flask import render_template

from flashlearn.db import connect


bp = Blueprint('home', __name__)

engine = connect()


@bp.route('/', methods=['GET'])
def home():

    decks = engine.execute('SELECT * FROM `deck`')

    return render_template('home.html', decks=decks)









