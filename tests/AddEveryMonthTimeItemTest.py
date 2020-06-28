import os
import unittest

from src.TodoBot import TodoBot
from src.models.EveryMonthTimeScheduleItem import EveryMonthTimeScheduleItem


class AddEveryMonthTimeItemTest(unittest.TestCase):

    def setUp(self) -> None:
        self.bot = TodoBot("sqlite:///../static/test_todo_bot.db")

    def tearDown(self) -> None:
        os.remove("../static/test_todo_bot.db")

    def test_add_one_item_interface(self):
        answer = self.bot.message_handler('++ 1 00:00 напоминание №1', '1')
        self.assertEqual('Добавлено напоминание о "напоминание №1" на 1 00:00', answer)

    def test_add_one_item_base(self):
        self.bot.message_handler('++ 1 00:00 напоминание №1', '1')
        item = self.bot.get_session().query(EveryMonthTimeScheduleItem).first()
        self.assertEqual('напоминание №1', item.name)
        self.assertEqual('1 00:00', item.notification_datetime)
