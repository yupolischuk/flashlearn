to run app with MySQL:
pip install pymysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_name'


>>> from flashcard import db
>>> db.create_all()
>>> exit()


TODO
Handling card leanring level (prioritization)
Card Decks
Flashcards with code, with syntax highlight
Nested Sets for Decks
Статистика
    сколько раз проголосовали в текущий день

Charts:
    commit(добавление карт) heatmap

Mindmapping

