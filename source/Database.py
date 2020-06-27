import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from source.models.Base import Base


class Database:
    __instance = None

    def __init__(self):
        with open('../static/config.json') as config_file:
            data = config_file.read()
            config = json.loads(data)
            self.engine = create_engine(config['database_name'])
            Base.metadata.create_all(self.engine)

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = Database()
        return cls.__instance

    @classmethod
    def new_base(cls):
        cls.__instance = Database()
        return cls.__instance

    def session(self) -> Session:
        return sessionmaker(bind=self.engine)()
