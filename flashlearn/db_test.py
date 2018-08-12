from sqlalchemy import create_engine, MetaData, Table

# engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)

file = open('./flashcard.cfg', 'r')
str = file.read()
arr = str.split("=")
config = arr[1][2:48]
engine = create_engine(config, convert_unicode=True)


metadata = MetaData(bind=engine)

from sqlalchemy import Table

# flashcard = Table('flashcard', metadata, autoload=True)

con = engine.connect()
# con.execute(users.insert(), name='admin', email='admin@localhost')

res = engine.execute('select * from flashcard where id = 2').first() # working
print(res)
