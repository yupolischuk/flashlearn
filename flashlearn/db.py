from sqlalchemy import create_engine, MetaData
import config

config =  config.SQLALCHEMY_DATABASE_URI


def connect():
    engine = create_engine(config, convert_unicode=True)
    metadata = MetaData(bind=engine)
    con = engine.connect()

    return engine



