import os
import unittest

from source.TodoBot import TodoBot
from source.models.Item import Item
from source.models.ItemState import ItemState
from source.models.List import List


class GetListTest(unittest.TestCase):

    def setUp(self) -> None:
        self.bot = TodoBot("sqlite:///../static/test_todo_bot.db")

    def tearDown(self) -> None:
        os.remove("../static/test_todo_bot.db")

    def test_get_empty_list_interface(self):
        answer = self.bot.message_handler('??', '1')
        self.assertEqual('Список пуст', answer)

    def test_get_list_with_one_item_interface(self):
        session = self.bot.get_session()
        list = List('1')
        session.add(list)
        session.commit()
        session.add(Item('дело №1', list))
        session.commit()
        answer = self.bot.message_handler('??', '1')
        self.assertEqual('1) дело №1', answer)

    def test_get_list_with_two_items_interface(self):
        session = self.bot.get_session()
        list = List('1')
        session.add(list)
        session.commit()
        session.add(Item('дело №1', list))
        session.add(Item('дело №2', list))
        session.commit()
        answer = self.bot.message_handler('??', '1')
        self.assertEqual('1) дело №1\n'
                         '2) дело №2', answer)

    def test_get_items_from_different_lists_interface(self):
        session = self.bot.get_session()
        list1 = List('1')
        session.add(list1)
        session.commit()
        session.add(Item('дело №1', list1))
        list2 = List('2')
        session.add(list2)
        session.commit()
        session.add(Item('дело №2', list2))
        session.commit()
        answer = self.bot.message_handler('??', '1')
        self.assertEqual('1) дело №1', answer)
        answer = self.bot.message_handler('??', '2')
        self.assertEqual('1) дело №2', answer)

    def test_get_list_with_one_mark_item_interface(self):
        session = self.bot.get_session()
        list = List('1')
        session.add(list)
        session.commit()
        session.add(Item('дело №1', list, state=ItemState.MARK))
        session.commit()
        answer = self.bot.message_handler('??', '1')
        self.assertEqual('<strike>1) дело №1</strike>', answer)

    def test_get_list_with_two_mark_item_interface(self):
        session = self.bot.get_session()
        list = List('1')
        session.add(list)
        session.commit()
        session.add(Item('дело №1', list, state=ItemState.MARK))
        session.add(Item('дело №2', list, state=ItemState.MARK))
        session.commit()
        answer = self.bot.message_handler('??', '1')
        self.assertEqual('<strike>1) дело №1</strike>\n'
                         '<strike>2) дело №2</strike>', answer)

    def test_get_list_with_one_mark_item_and_one_item_interface(self):
        session = self.bot.get_session()
        list = List('1')
        session.add(list)
        session.commit()
        session.add(Item('дело №1', list, state=ItemState.MARK))
        session.add(Item('дело №2', list))
        session.commit()
        answer = self.bot.message_handler('??', '1')
        self.assertEqual('<strike>1) дело №1</strike>\n'
                         '2) дело №2', answer)

    def test_get_list_with_one_item_and_one_mark_item_interface(self):
        session = self.bot.get_session()
        list = List('1')
        session.add(list)
        session.commit()
        session.add(Item('дело №1', list))
        session.add(Item('дело №2', list, state=ItemState.MARK))
        session.commit()
        answer = self.bot.message_handler('??', '1')
        self.assertEqual('1) дело №1\n'
                         '<strike>2) дело №2</strike>', answer)

    def test_get_list_with_one_item_and_one_delete_item_interface(self):
        session = self.bot.get_session()
        list = List('1')
        session.add(list)
        session.commit()
        session.add(Item('дело №1', list))
        session.add(Item('дело №2', list, state=ItemState.DELETE))
        session.commit()
        answer = self.bot.message_handler('??', '1')
        self.assertEqual('1) дело №1', answer)
