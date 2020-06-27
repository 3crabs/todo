from sqlalchemy import Integer, Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from source.models.Base import Base
from source.models.List import List


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    list_id = Column(Integer, ForeignKey("lists.id"))
    list = relationship("List")
    state = Column(String)

    def __init__(self, name: str, list: List, state: str = 'active'):
        self.name = name
        self.list = list
        self.state = state
