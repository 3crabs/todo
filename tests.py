import unittest

import bot
from bot import content_text_answer


class FunctionalTest(unittest.TestCase):

    def setUp(self) -> None:
        bot.data_base = []

    def tearDown(self):
        bot.data_base = []

    def test_add_todo_item(self):
        answer = content_text_answer('бот добавь дело №1')
        self.assertEqual('дело №1 добавлено', answer)
        self.assertEqual(1, len(bot.data_base))

    def test_delete_todo_item(self):
        content_text_answer('бот добавь дело №1')
        answer = content_text_answer('бот удали 1')
        self.assertEqual('дело №1 удалено', answer)
        self.assertEqual(0, len(bot.data_base))

    def test_get_empty_list(self):
        answer = content_text_answer('бот покажи список')
        self.assertEqual('Ваш список пока пуст', answer)
        self.assertEqual(0, len(bot.data_base))

    def test_get_list_with_one_item(self):
        bot.data_base.append('дело №1')
        answer = content_text_answer('бот покажи список')
        self.assertIn('1) дело №1', answer)

    def test_add_item_and_get_list(self):
        content_text_answer('бот добавь дело №1')
        answer = content_text_answer('бот покажи список')
        self.assertIn('1) дело №1', answer)
