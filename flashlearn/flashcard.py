from flask import Blueprint
from flask import render_template
from flask import request
from flask import jsonify

from flashlearn.db import connect
from flashlearn.helper import current_timestamp

bp = Blueprint('flashcard', __name__)

engine = connect()

@bp.route('/flashcard/test')
def test():
    # db = get_db()
    # posts = db.execute(
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' ORDER BY created DESC'
    # ).fetchall()
    # return render_template('blog/index.html', posts=posts)
    res = engine.execute('select * from flashcard where id = 2').first()
    print(res)

    print(type(res[2]))
    return res[2]


# TODO CARD CRUD
@bp.route('/flashcard/', methods=['GET'])
def index():
    id = request.args.get('id')

    # TODO validate params to prevent SQL injections
    flashcard = engine.execute('SELECT * FROM `flashcard` WHERE id = ' + str(id)).first()

    # print(flashcard['id'])

    return render_template('flashcard.html', flashcard=flashcard)


@bp.route('/flashcard/update', methods=['POST'])
def update():
    id = request.form.get('id')

    print('7777777777777777777777777777777')
    print(id)

    return 'hi'


