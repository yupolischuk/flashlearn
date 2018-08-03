import os

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_name'


db = SQLAlchemy(app)

class Flashcard(db.Model):
    __tablename__ = 'flashcard'
    # __table_args__ = (
    #     {'mysql_character_set': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_520_ci'},
    # )
    question = db.Column(db.String(255), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Question: {}>".format(self.question)


@app.route('/', methods=["GET", "POST"])
def home():
    flashcards = None
    if request.form:
        try:
            flashcard = Flashcard(question=request.form.get("question"))
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
        oldquestion = request.form.get("oldquestion")
        flashcard = Flashcard.query.filter_by(question=oldquestion).first()
        flashcard.question = newquestion
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


if __name__ == "__main__":
    app.run(debug=True)
