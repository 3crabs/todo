from sqlalchemy import Integer, Column, String

from source.models.Base import Base


class List(Base):
    __tablename__ = 'lists'
    id = Column(Integer, primary_key=True)
    chat_id = Column(String)

    def __init__(self, chat_id: str):
        self.chat_id = chat_id
