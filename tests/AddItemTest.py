import os
import unittest

from source.TodoBot import TodoBot
from source.models.Item import Item
from source.models.List import List


class AddItemTest(unittest.TestCase):

    def setUp(self) -> None:
        self.bot = TodoBot("sqlite:///../static/test_todo_bot.db")

    def tearDown(self) -> None:
        os.remove("../static/test_todo_bot.db")

    def test_add_one_item_interface(self):
        answer = self.bot.message_handler('++ дело №1', '1')
        self.assertEqual('Добавлено "дело №1"', answer)

    def test_add_one_item_interface_2(self):
        answer = self.bot.message_handler('++ дело №2', '1')
        self.assertEqual('Добавлено "дело №2"', answer)

    def test_add_one_item_base(self):
        self.bot.message_handler('++ дело №1', '1')
        item = self.bot.get_session().query(Item).first()
        self.assertEqual('дело №1', item.name)
        self.assertEqual('1', item.list.chat_id)

    def test_add_one_item_base_2(self):
        self.bot.message_handler('++ дело №2', '2')
        item = self.bot.get_session().query(Item).first()
        self.assertEqual('дело №2', item.name)
        self.assertEqual('2', item.list.chat_id)

    def test_add_two_items_base(self):
        self.bot.message_handler('++ дело №1', '1')
        self.bot.message_handler('++ дело №2', '1')
        lists = self.bot.get_session().query(List).all()
        self.assertEqual(1, len(lists))
