import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.models.Base import Base


def create_database(test=False):
    with open('../static/config.json') as config_file:
        data = config_file.read()
        config = json.loads(data)
        if test:
            database_name = config['test_database_name']
        else:
            database_name = config['database_name']
        engine = create_engine(database_name)
        Base.metadata.create_all(engine)


def connect_and_get_session(test=False) -> Session:
    with open('../static/config.json') as config_file:
        data = config_file.read()
        config = json.loads(data)
        if test:
            database_name = config['test_database_name']
        else:
            database_name = config['database_name']
        engine = create_engine(database_name)
        Base.metadata.create_all(engine)
        return sessionmaker(bind=engine)()
