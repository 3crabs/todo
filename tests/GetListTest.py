import unittest

from source.Database import Database
from source.models.Item import Item
from source.models.List import List
from source.run_bot import message_handler


class GetListTest(unittest.TestCase):

    def setUp(self) -> None:
        self.session = Database.new_base().session()

    def test_get_empty_list_interface(self):
        answer = message_handler('??', '1')
        self.assertEqual('Список пуст', answer)

    def test_get_list_with_one_item_interface(self):
        list = List('1')
        self.session.add(list)
        self.session.commit()
        self.session.add(Item('дело №1', list))
        self.session.commit()
        answer = message_handler('??', '1')
        self.assertEqual('1) дело №1', answer)

    def test_get_list_with_two_items_interface(self):
        list = List('1')
        self.session.add(list)
        self.session.commit()
        self.session.add(Item('дело №1', list))
        self.session.add(Item('дело №2', list))
        self.session.commit()
        answer = message_handler('??', '1')
        self.assertEqual('1) дело №1\n'
                         '2) дело №2', answer)
