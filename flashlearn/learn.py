from flask import ( Blueprint)
from flashlearn.db import connect

bp = Blueprint('learn', __name__)


@bp.route('/learn/test')
def test():

    engine = connect()
    res = engine.execute('select * from flashcard where id = 2').first()

    return res[2]

