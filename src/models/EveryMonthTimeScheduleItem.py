from sqlalchemy import Integer, Column, String

from src.models.Base import Base
from src.models.ItemState import ItemState


class EveryMonthTimeScheduleItem(Base):
    __tablename__ = 'every_month_time_schedules'
    id = Column(Integer, primary_key=True)
    chat_id = Column(String)
    name = Column(String)
    notification_datetime = Column(String)
    state = Column(String)

    def __init__(self, chat_id: str, name: str, notification_datetime: str, state: str = ItemState.ACTIVE):
        self.chat_id = chat_id
        self.name = name
        self.notification_datetime = notification_datetime
        self.state = state
