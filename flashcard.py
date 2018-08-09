import os
import time, datetime

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

app.config.from_pyfile('flashcard.cfg')

db = SQLAlchemy(app)

class Flashcard(db.Model):
    __tablename__ = 'flashcard'
    # __table_args__ = (
    #     {'mysql_character_set': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_520_ci'},
    # )
    id = db.Column(db.INTEGER)
    question = db.Column(db.String(255), unique=False, nullable=False, primary_key=True)
    answer = db.Column(db.String())
    updated = db.Column(db.TIMESTAMP)
    level = db.Column(db.INTEGER)


    def __repr__(self):
        return "<Question: {}>".format(self.question)


@app.route('/', methods=["GET", "POST"])
def home():
    flashcards = None
    if request.form:
        try:
            flashcard = Flashcard(question=request.form.get("question"),
                                  answer=request.form.get("answer"))
            db.session.add(flashcard)
            db.session.commit()
        except Exception as e:
            print("Failed to add flashcard")
            print(e)
    flashcards = Flashcard.query.all()

    return render_template("index.html", flashcards=flashcards)


@app.route("/update", methods=["POST"])
def update():
    try:
        newquestion = request.form.get("newquestion")
        newanswer = request.form.get("newanswer")
        oldquestion = request.form.get("oldquestion")

        flashcard = Flashcard.query.filter_by(question=oldquestion).first()
        flashcard.question = newquestion
        flashcard.answer = newanswer
        db.session.commit()
    except Exception as e:
        print("Couldn't update flashcard question")
        print(e)

    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    question = request.form.get("question")
    flashcard = Flashcard.query.filter_by(question=question).first()
    db.session.delete(flashcard)
    db.session.commit()
    return redirect("/")


@app.route("/learning", methods=["GET"])
def learn():
    return render_template("learning.html")


@app.route("/give_card", methods=["POST"])
def give_card():
    card_id = int(request.form.get("card_id"))
    action = request.form.get('action')

    '''
    Приоритет выдачи карт
    Выбрать все из выбранной колоды которые
        отвечал больше дня назад + начиная из самого низкого уровня
        выбираем все обновленные сегодня но больше часа назад + начиная из самого низкого уровня
        выбираем все обновленные меньше часа назад + начная из самого низкого уровня
        
    '''
    # engine.execute('select * from flashcard where id=5').first()  # get flashcard as list of tuples
    # engine.execute('select min(id) from flashcard where id > 4').first()  # get next id after 4th

    # Get next card id and send to client
    # id=4
    # result = db.engine.execute("select min(id) from flashcard where id = '%id'" %id).first()
    # return str(result[0])

    # return jsonify([fcard.id, fcard.question, fcard.answer])


    if action == 'give_first':
        # card = Flashcard.query.filter_by(id=card_id).first()
        # return jsonify([card.id, card.question, card.answer, card.level])

        # Выбрать первую, у которой min(level)
        # SELECT * FROM `flashcard` WHERE level = (SELECT MIN(level) AS LovestLevel FROM `flashcard`);
        sql = 'SELECT * FROM `flashcard` WHERE level = (SELECT MIN(level) FROM `flashcard`)'
        card = db.engine.execute(sql).first()
        return jsonify([str(card[0]), str(card[1]), str(card[2]), str(card[4])])

    elif action == 'give_next':
        current = str(card_id)
        current_level = db.engine.execute("SELECT level FROM flashcard WHERE id = " + current).first()

        next_id = db.engine.execute(
            "SELECT MIN(id) FROM flashcard "
            "WHERE id > " + current + " AND level = " + str(current_level[0])
        ).first()

        if next_id[0] is None:
            next_id = db.engine.execute(
                "SELECT MIN(id) FROM flashcard "
                "WHERE id > " + current + " AND level = 2").first()
            print('77777777777777777777777777777')
            print(next_id)

        if next_id[0]:
            card = Flashcard.query.filter_by(id=next_id[0]).first()
            return jsonify([card.id, card.question, card.answer, card.level])
        else:
            return 'card not found'

    elif action == 'give_prev':
        current = str(card_id)
        current_level = db.engine.execute("SELECT level FROM flashcard WHERE id = " + current).first()
        # prev_id_same_level = db.engine.execute("SELECT MAX(id) FROM flashcard WHERE id <" + current + " AND level = 1").first()
        prev_id_same_level = db.engine.execute(
            "SELECT MAX(id) FROM flashcard "
            "WHERE id < " + current + " AND level = " + str(current_level[0])
        ).first()
        card = Flashcard.query.filter_by(id=prev_id_same_level[0]).first()
        return jsonify([card.id, card.question, card.answer, card.level])


@app.route("/set_level", methods=["POST"])
def update_level():
    # TODO exception handling and sending operation status
    # fcard_id = request.args.get('fcard_id') # if send through postfix
    card_id = request.form.get('card_id')
    level = request.form.get('level')
    flashcard = Flashcard.query.filter_by(id=card_id).first()
    flashcard.level = level
    flashcard.updated = current_timestamp()
    db.session.commit()

    return jsonify([card_id, level])


    # Catch json request
    # res = request.get_json(force=True)
    #
    # print('8888888888888888888888888888888')
    # print(res)
    # print('8888888888888888888888888888888')
    # return 'JSON posted'


def current_timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return st


if __name__ == "__main__":
    app.run(debug=True)
