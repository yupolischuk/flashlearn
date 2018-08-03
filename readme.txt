to run app with MySQL:
pip install pymysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_name'


>>> from flashcard import db
>>> db.create_all()
>>> exit()
