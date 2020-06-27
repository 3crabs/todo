import unittest

from source.Database import Database
from source.models.Item import Item
from source.models.ItemState import ItemState
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

    def test_get_items_from_different_lists_interface(self):
        list1 = List('1')
        self.session.add(list1)
        self.session.commit()
        self.session.add(Item('дело №1', list1))
        list2 = List('2')
        self.session.add(list2)
        self.session.commit()
        self.session.add(Item('дело №2', list2))
        self.session.commit()
        answer = message_handler('??', '1')
        self.assertEqual('1) дело №1', answer)
        answer = message_handler('??', '2')
        self.assertEqual('1) дело №2', answer)

    def test_get_list_with_one_mark_item_interface(self):
        list = List('1')
        self.session.add(list)
        self.session.commit()
        self.session.add(Item('дело №1', list, state=ItemState.MARK))
        self.session.commit()
        answer = message_handler('??', '1')
        self.assertEqual('<strike>1) дело №1</strike>', answer)

    def test_get_list_with_two_mark_item_interface(self):
        list = List('1')
        self.session.add(list)
        self.session.commit()
        self.session.add(Item('дело №1', list, state=ItemState.MARK))
        self.session.add(Item('дело №2', list, state=ItemState.MARK))
        self.session.commit()
        answer = message_handler('??', '1')
        self.assertEqual('<strike>1) дело №1</strike>\n'
                         '<strike>2) дело №2</strike>', answer)

    def test_get_list_with_one_mark_item_and_one_item_interface(self):
        list = List('1')
        self.session.add(list)
        self.session.commit()
        self.session.add(Item('дело №1', list, state=ItemState.MARK))
        self.session.add(Item('дело №2', list))
        self.session.commit()
        answer = message_handler('??', '1')
        self.assertEqual('<strike>1) дело №1</strike>\n'
                         '2) дело №2', answer)

    def test_get_list_with_one_item_and_one_mark_item_interface(self):
        list = List('1')
        self.session.add(list)
        self.session.commit()
        self.session.add(Item('дело №1', list))
        self.session.add(Item('дело №2', list, state=ItemState.MARK))
        self.session.commit()
        answer = message_handler('??', '1')
        self.assertEqual('1) дело №1\n'
                         '<strike>2) дело №2</strike>', answer)

    def test_get_list_with_one_item_and_one_delete_item_interface(self):
        list = List('1')
        self.session.add(list)
        self.session.commit()
        self.session.add(Item('дело №1', list))
        self.session.add(Item('дело №2', list, state=ItemState.DELETE))
        self.session.commit()
        answer = message_handler('??', '1')
        self.assertEqual('1) дело №1', answer)
