import unittest

import bot
from bot import content_text_answer


class FunctionalTest(unittest.TestCase):

    def setUp(self) -> None:
        bot.data_base = {}

    def tearDown(self):
        bot.data_base = {}

    def test_add_todo_item(self):
        answer = content_text_answer('бот добавь дело №1', '1')
        self.assertEqual('дело №1 добавлено', answer)
        self.assertEqual(1, len(bot.data_base))
        self.assertEqual(1, len(bot.data_base['1']))
        self.assertEqual('дело №1', bot.data_base['1'][0])

    def test_delete_todo_item(self):
        bot.data_base = {'1': ['дело №1']}
        answer = content_text_answer('бот удали 1', '1')
        self.assertEqual('дело №1 удалено', answer)
        self.assertEqual(0, len(bot.data_base))

    def test_get_empty_list(self):
        answer = content_text_answer('бот покажи список', '1')
        self.assertEqual('Ваш список пока пуст', answer)
        self.assertEqual(0, len(bot.data_base))

    def test_add_item_and_get_list(self):
        content_text_answer('бот добавь дело №1', '1')
        answer = content_text_answer('бот покажи список', '1')
        self.assertIn('1) дело №1', answer)

        answer = content_text_answer('бот покажи список', '2')
        self.assertIn('Ваш список пока пуст', answer)

    def test_text(self):
        answer = content_text_answer('бот', '1')
        self.assertEqual('', answer)

    def test_short_add_item(self):
        answer = content_text_answer('+ дело №1', '1')
        self.assertEqual('дело №1 добавлено', answer)
        self.assertEqual(1, len(bot.data_base))
        self.assertEqual(1, len(bot.data_base['1']))
        self.assertEqual('дело №1', bot.data_base['1'][0])

    def test_short_delete_todo_item(self):
        bot.data_base = {'1': ['дело №1']}
        answer = content_text_answer('- 1', '1')
        self.assertEqual('дело №1 удалено', answer)
        self.assertEqual(0, len(bot.data_base))