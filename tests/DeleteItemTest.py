import unittest

from source.Database import Database
from source.models.Item import Item
from source.models.ItemState import ItemState
from source.models.List import List
from source.run_bot import message_handler


class DeleteItemTest(unittest.TestCase):

    def setUp(self) -> None:
        self.session = Database.new_base().session()

    def test_delete_item_interface(self):
        list = List('1')
        self.session.add(list)
        self.session.commit()
        self.session.add(Item('дело №1', list))
        self.session.commit()
        answer = message_handler('-- 1', '1')
        self.assertEqual('Удалено "дело №1"', answer)

    def test_delete_item_interface_2(self):
        list = List('1')
        self.session.add(list)
        self.session.commit()
        self.session.add(Item('дело №2', list))
        self.session.commit()
        answer = message_handler('-- 1', '1')
        self.assertEqual('Удалено "дело №2"', answer)

    def test_delete_one_item_interface_3(self):
        answer = message_handler('-- 1', '1')
        self.assertEqual('Элемента с номером 1 нет в вашем списке', answer)

    def test_delete_one_item_interface_4(self):
        answer = message_handler('-- -1', '1')
        self.assertEqual('Элемента с номером -1 не может быть в вашем списке', answer)

    def test_delete_one_item_interface_5(self):
        answer = message_handler('-- 2', '1')
        self.assertEqual('Элемента с номером 2 нет в вашем списке', answer)

    def test_delete_one_item_interface_6(self):
        answer = message_handler('-- -2', '1')
        self.assertEqual('Элемента с номером -2 не может быть в вашем списке', answer)

    def test_delete_one_item_interface_7(self):
        answer = message_handler('-- первый', '1')
        self.assertEqual('"первый" непохоже на номер в списке', answer)

    def test_delete_one_item_interface_8(self):
        answer = message_handler('-- второй', '1')
        self.assertEqual('"второй" непохоже на номер в списке', answer)

    def test_delete_all_items_interface(self):
        answer = message_handler('---', '1')
        self.assertEqual('Все элементы удалены', answer)

    def test_delete_all_items_base(self):
        list = List('1')
        self.session.add(list)
        self.session.commit()
        item = Item('дело №1', list)
        self.session.add(item)
        self.session.commit()
        message_handler('---', '1')
        self.assertEqual(ItemState.DELETE, item.state)

    def test_delete_all_items_base_2(self):
        list = List('1')
        self.session.add(list)
        self.session.commit()
        item = Item('дело №1', list)
        self.session.add(item)
        self.session.commit()
        message_handler('---', '2')
        self.assertEqual(ItemState.ACTIVE, item.state)

    def test_delete_all_mark_items_base(self):
        list = List('1')
        self.session.add(list)
        self.session.commit()
        item = Item('дело №1', list, ItemState.MARK)
        self.session.add(item)
        self.session.commit()
        message_handler('--*', '1')
        self.assertEqual(ItemState.DELETE, item.state)

    def test_delete_all_mark_items_base_2(self):
        list = List('1')
        self.session.add(list)
        self.session.commit()
        item = Item('дело №1', list, ItemState.ACTIVE)
        self.session.add(item)
        self.session.commit()
        message_handler('--*', '1')
        self.assertEqual(ItemState.ACTIVE, item.state)
