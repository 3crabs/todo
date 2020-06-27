import os
import unittest

from source.TodoBot import TodoBot
from source.models.Item import Item
from source.models.ItemState import ItemState
from source.models.List import List


class MarkItemTest(unittest.TestCase):

    def setUp(self) -> None:
        self.bot = TodoBot("sqlite:///../static/test_todo_bot.db")

    def tearDown(self) -> None:
        os.remove("../static/test_todo_bot.db")

    def test_mark_one_item_interface(self):
        session = self.bot.get_session()
        list = List('1')
        session.add(list)
        session.commit()
        session.add(Item('дело №1', list))
        session.commit()
        answer = self.bot.message_handler('** 1', '1')
        self.assertEqual('Зачеркнуто "дело №1"', answer)

    def test_mark_one_item_interface_2(self):
        session = self.bot.get_session()
        list = List('1')
        session.add(list)
        session.commit()
        session.add(Item('дело №2', list))
        session.commit()
        answer = self.bot.message_handler('** 1', '1')
        self.assertEqual('Зачеркнуто "дело №2"', answer)

    def test_mark_one_item_interface_3(self):
        answer = self.bot.message_handler('** 1', '1')
        self.assertEqual('Элемента с номером 1 нет в вашем списке', answer)

    def test_mark_one_item_interface_4(self):
        answer = self.bot.message_handler('** -1', '1')
        self.assertEqual('Элемента с номером -1 не может быть в вашем списке', answer)

    def test_mark_one_item_interface_5(self):
        answer = self.bot.message_handler('** 2', '1')
        self.assertEqual('Элемента с номером 2 нет в вашем списке', answer)

    def test_mark_one_item_interface_6(self):
        answer = self.bot.message_handler('** -2', '1')
        self.assertEqual('Элемента с номером -2 не может быть в вашем списке', answer)

    def test_mark_one_item_interface_7(self):
        answer = self.bot.message_handler('** первый', '1')
        self.assertEqual('"первый" непохоже на номер в списке', answer)

    def test_mark_one_item_interface_8(self):
        answer = self.bot.message_handler('** второй', '1')
        self.assertEqual('"второй" непохоже на номер в списке', answer)

    def test_delete_all_items_interface(self):
        answer = self.bot.message_handler('--*', '1')
        self.assertEqual('Все зачеркнутые элементы удалены', answer)

    def test_mark_one_item_base(self):
        session = self.bot.get_session()
        list = List('1')
        session.add(list)
        session.commit()
        item = Item('дело №1', list)
        session.add(item)
        session.commit()
        self.bot.message_handler('** 1', '1')
        self.assertEqual(ItemState.MARK, item.state)
