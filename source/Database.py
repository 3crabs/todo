import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from source.models.Base import Base


class Database:
    __instance = None

    def __init__(self, test):
        with open('../static/config.json') as config_file:
            data = config_file.read()
            config = json.loads(data)
            if test:
                self.engine = create_engine(config['test_database_name'])
            else:
                self.engine = create_engine(config['database_name'])
            Base.metadata.create_all(self.engine)

    @classmethod
    def get_instance(cls):
        return cls.__instance

    @classmethod
    def new_base(cls, test=True):
        cls.__instance = Database(test)
        return cls.__instance

    def session(self) -> Session:
        return sessionmaker(bind=self.engine)()
