from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect

from flashlearn.db import connect
from flashlearn.helper import current_timestamp

bp = Blueprint('flashcard', __name__)

engine = connect()


# Create
@bp.route('/flashcard/create/', methods=['GET'])
def create():
    decks = engine.execute("SELECT * FROM `deck`")

    return render_template('flashcard/create.html', decks=decks)


@bp.route('/flashcard/save_new/', methods=['POST'])
def save_new():
    level = 1
    updated = current_timestamp()
    question = request.form.get('question')
    answer = request.form.get('answer')
    deck_id = request.form.get('deck_id')

    sql = "INSERT INTO `flashcard`(`question`, `answer`, `level`, `deck_id`) " \
          "VALUES (\'" + question + "\', \'" + answer + "\', \'" + str(level) + "\', \'" + str(deck_id) + "\'" + ")"

    engine.execute(sql)

    return 'success'


# Update
@bp.route('/flashcard/update/', methods=['GET'])
def update():

    id = request.args.get('id')
    sql = "SELECT id, question, answer, deck_id FROM `flashcard` WHERE id=" + id
    flashcard = engine.execute(sql).first()

    sql_decks = "SELECT * FROM deck"
    decks = engine.execute(sql_decks)

    return render_template('flashcard/update.html', flashcard=flashcard, decks=decks)


@bp.route('/flashcard/update/', methods=['POST'])
def save_changes():

    id = request.form.get('id')
    question = request.form.get('question')
    answer = request.form.get('answer')
    deck_id = request.form.get('deck_id')
    updated = current_timestamp()

    sql = "UPDATE `flashcard` SET question=\'" + question + "\', answer=\'" + answer + \
          "\', deck_id=\'" + deck_id + "\', updated=\'" + updated + "\' WHERE id=" + id

    print('777777777777777777777777777777777777')
    print(sql)


    engine.execute(sql)

    return redirect('/')


# @bp.route('/flashcard/update/', methods=['POST'])
# def update():
#
#     id = request.form.get('id')
#     question = request.form.get('question')
#     answer = request.form.get('answer')
#     level = request.form.get('level')
#     updated = current_timestamp()
#
#     str = 'UPDATE `flashcard` SET `question`=\'' + question + '\',`answer`=\'' + answer +\
#         '\',`updated`=\'' + updated + '\',`level`=\'' + level + '\' WHERE id=' + id
#
#     engine.execute(str)
#
#     return 'hi'


# Delete
@bp.route('/flashcard/delete/', methods=['POST'])
def delete():

    id = request.form.get('id')
    engine.execute('DELETE FROM `flashcard` WHERE id=' + id)

    return 'deleted'
    # return redirect('/')


