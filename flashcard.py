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
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), unique=True, nullable=False, primary_key=True)
    answer = db.Column(db.String(255), unique=True, nullable=False, primary_key=True)


    def __repr__(self):
        return "<Question: {}>".format(self.question)


if __name__ == "__main__":
    app.run(debug=True)
