to run app with MySQL:
pip install pymysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_name'


>>> from flashcard import db
>>> db.create_all()
>>> exit()


TODO
Refector
    Make app structure http://exploreflask.com/en/latest/organizing.html

Handling card leanring level (prioritization)
Card Decks
Flashcards with code, with syntax highlight
Adding images to cards
Nested Sets for Decks

Статистика
    сколько раз проголосовали в текущий день

Charts:
    commit(добавление карт) heatmap

Mindmapping
Block-scheme painting
