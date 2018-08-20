from flask import Blueprint
from flask import render_template

from flashlearn.db import connect


bp = Blueprint('home', __name__)

engine = connect()


@bp.route('/', methods=['GET'])
def home():
    # TODO think how to rewrite without nested dictionary
    decks_obj = engine.execute('SELECT * FROM `deck`')
    counted_cards_obj = engine.execute('SELECT deck_id as id, count(*) as count_card FROM `flashcard` GROUP BY deck_id')

    decks = db_obj_to_dict(decks_obj)
    counted_cards = db_obj_to_dict(counted_cards_obj)

    # add counted cards to all decks
    for key, value in decks.items():
        if key in counted_cards:
            value['count_cards'] = counted_cards[key].get('count_card')
        else:
            value['count_cards'] = 0

    return render_template('home.html', decks=decks.values())


def db_obj_to_dict(db_obj):
    # creating dictionary from SQLAlchemy object: keys is ids values in rows
    res = {}
    for row in db_obj:
        row = dict(row)
        res[row.get('id')] = row

    return res







