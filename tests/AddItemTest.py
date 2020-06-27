import unittest

from source.run_bot import message_handler


class AddItemTest(unittest.TestCase):

    def test_add_one_item_interface(self):
        answer = message_handler('++ дело №1', '1')
        self.assertEqual('Добавлено "дело №1"', answer)

    def test_add_one_item_interface_2(self):
        answer = message_handler('++ дело №2', '1')
        self.assertEqual('Добавлено "дело №2"', answer)
