from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect

from flashlearn.helper import current_timestamp


from flashlearn.db import connect

bp = Blueprint('deck', __name__)

engine = connect()


# Watch
@bp.route('/deck/watch/', methods=['GET'])
def watch():

    id = request.args.get('id')
    sql = "SELECT * FROM `flashcard` WHERE deck_id=" + str(id)
    flashcards = engine.execute(sql)

    return render_template('deck/watch.html', flashcards=flashcards, deck_id=id)


# Create
@bp.route('/deck/create/', methods=['GET'])
def create_page():

    return render_template('deck/create.html')


@bp.route('/deck/create/', methods=['POST'])
def save_new():

    name = request.form.get('name')
    sql = "INSERT INTO `deck` (`name`) VALUES ( '" + str(name) + "');"
    engine.execute(sql)

    return redirect('/')


# Update
@bp.route('/deck/update/', methods=['GET'])
def update():

    id = request.args.get('id')
    sql = "SELECT id, name FROM `deck` WHERE id=" + id
    deck = engine.execute(sql).first()

    return render_template('deck/update.html', deck=deck)


@bp.route('/deck/update/', methods=['POST'])
def save_changes():

    id = request.form.get('id')
    name = request.form.get('name')
    updated = current_timestamp()

    sql = "UPDATE `deck` SET `name`=\'" + name + "\', `updated`=\'" + updated + "\' WHERE id=" + id
    engine.execute(sql)

    return redirect('/')


# Delete
@bp.route('/deck/delete/', methods=['POST'])
def delete():

    id = request.form.get('id')
    sql = "DELETE FROM `deck` WHERE id=" + str(id)
    engine.execute(sql)

    return 'success'






