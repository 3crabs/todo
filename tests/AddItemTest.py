import unittest

from source.Database import Database
from source.models.Item import Item
from source.run_bot import message_handler


class AddItemTest(unittest.TestCase):

    def setUp(self) -> None:
        self.session = Database.new_base().session()

    def test_add_one_item_interface(self):
        answer = message_handler('++ дело №1', '1')
        self.assertEqual('Добавлено "дело №1"', answer)

    def test_add_one_item_interface_2(self):
        answer = message_handler('++ дело №2', '1')
        self.assertEqual('Добавлено "дело №2"', answer)

    def test_add_one_item_base(self):
        message_handler('++ дело №1', '1')
        item = self.session.query(Item).first()
        self.assertEqual('дело №1', item.name)
        self.assertEqual('1', item.list.chat_id)

    def test_add_one_item_base_2(self):
        message_handler('++ дело №2', '2')
        item = self.session.query(Item).first()
        self.assertEqual('дело №2', item.name)
        self.assertEqual('2', item.list.chat_id)
