to run app with MySQL:
pip install pymysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_name'


>>> from flashcard import db
>>> db.create_all()
>>> exit()


TODO
+Add Decks
+Add temporary table for learning session
Refactor
    Make app structure http://exploreflask.com/en/latest/organizing.html
Write Tests
+Handling card leanring level
Add 404 page
Add new type of cards (with code) with syntax highlight
Uploading images for cards
Nested Sets for Decks
User authorization

Статистика
    сколько раз проголосовали в текущий день

Charts:
    commit(добавление карт) heatmap

Mindmapping
Block-scheme painting
