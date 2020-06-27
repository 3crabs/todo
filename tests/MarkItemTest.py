import unittest

from source.Database import Database
from source.models.Item import Item
from source.models.List import List
from source.run_bot import message_handler


class MarkItemTest(unittest.TestCase):

    def setUp(self) -> None:
        self.session = Database.new_base().session()

    def test_mark_one_item_interface(self):
        list = List('1')
        self.session.add(list)
        self.session.commit()
        self.session.add(Item('дело №1', list))
        self.session.commit()
        answer = message_handler('** 1', '1')
        self.assertEqual('Отмечено "дело №1"', answer)

    def test_mark_one_item_interface_2(self):
        list = List('1')
        self.session.add(list)
        self.session.commit()
        self.session.add(Item('дело №2', list))
        self.session.commit()
        answer = message_handler('** 1', '1')
        self.assertEqual('Отмечено "дело №2"', answer)
