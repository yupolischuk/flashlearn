import os

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
    repetition_level = db.Column(db.INTEGER)


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
    # TODO if current_id empty return first else - next if current is last - return first
    flashcard = Flashcard.query.first()

    return render_template("learning.html", flashcard=flashcard)


@app.route("/update_repetition_level", methods=["POST"])
def update_repetition_level():
    # fcard_id = request.args.get('fcard_id') # if send through postfix
    fcard_id = request.form.get('fcard_id')
    repetition_level = request.form.get('repetition_level')



    flashcard = Flashcard.query.filter_by(id=fcard_id).first()
    flashcard.repetition_level = repetition_level
    db.session.commit()


    return jsonify([fcard_id, repetition_level])


    # Catch json request
    # res = request.get_json(force=True)
    #
    # print('8888888888888888888888888888888')
    # print(res)
    # print('8888888888888888888888888888888')
    # return 'JSON posted'


if __name__ == "__main__":
    app.run(debug=True)
