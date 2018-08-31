from flask import Blueprint
from flask import jsonify

from flashlearn.db import connect


bp = Blueprint('test_rest', __name__)
engine = connect()


@bp.route('/test_rest/', methods=['GET', 'POST'])
def index():
    decks_obj = engine.execute('SELECT * FROM `deck`')
    decks = []

    for deck in decks_obj:
        item = {'id': deck['id'], 'name': deck['name']}
        decks.append(item)

    return jsonify(decks)

