from flask import Blueprint
from flask import render_template
from flask import request

from flashlearn.db import connect
from flashlearn.helper import current_timestamp

bp = Blueprint('flashcard', __name__)

engine = connect()


# Create
@bp.route('/flashcard/create/', methods=['GET'])
def create():

    return render_template('flashcard/create.html')

@bp.route('/flashcard/save_new/', methods=['POST'])
def save_new():
    level = 1
    updated = current_timestamp()
    question = request.form.get('question')
    answer = request.form.get('answer')

    sql = "INSERT INTO `flashcard`(`question`, `answer`, `updated`, `level`) " \
          "VALUES (\'" + question + "\', \'" + answer + "\', \'" + updated + "\', " + str(level) + ")"
    engine.execute(sql);

    return 'hi'


# Update
@bp.route('/flashcard/update/', methods=['POST'])
def update():

    id = request.form.get('id')
    question = request.form.get('question')
    answer = request.form.get('answer')
    level = request.form.get('level')
    updated = current_timestamp()

    str = 'UPDATE `flashcard` SET `question`=\'' + question + '\',`answer`=\'' + answer +\
        '\',`updated`=\'' + updated + '\',`level`=\'' + level + '\' WHERE id=' + id

    engine.execute(str)

    return 'hi'


# Delete
@bp.route('/flashcard/delete/', methods=['POST'])
def delete():

    id = request.form.get('id')
    engine.execute('DELETE FROM `flashcard` WHERE id=' + id)

    return 'deleted'
    # return redirect('/')


