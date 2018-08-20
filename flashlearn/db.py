from sqlalchemy import create_engine, MetaData

file = open('./flashcard.cfg', 'r')
str = file.read()
arr = str.split("=")
config = arr[1][2:49]

def connect():
    engine = create_engine(config, convert_unicode=True)
    metadata = MetaData(bind=engine)
    con = engine.connect()

    return engine



