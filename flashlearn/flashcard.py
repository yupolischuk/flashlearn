from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort


from sqlalchemy import create_engine, MetaData, Table

# TODO WRITE HUMAN CONFIG INCLUDING
file = open('./flashcard.cfg', 'r')
str = file.read()
arr = str.split("=")
config = arr[1][2:49]

engine = create_engine(config, convert_unicode=True)

metadata = MetaData(bind=engine)
con = engine.connect()

# from flashlearn.db import get_db

bp = Blueprint('flashcard', __name__)

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

    # return 'Hi!!!!777777777777777777777!!!!!!!!7777777777777'

# TODO CARD CRUD
