import unittest

import bot
from bot import content_text_answer


class FunctionalTest(unittest.TestCase):

    def setUp(self) -> None:
        bot.data_base_lists = {}

    def tearDown(self) -> None:
        bot.data_base_lists = {}

    def test_add_todo_item_answer(self):
        answer, keyoard = content_text_answer('бот добавь дело №1', '1')
        self.assertEqual('дело №1 добавлено', answer)

    def test_add_todo_item_base(self):
        content_text_answer('бот добавь дело №1', '1')
        self.assertEqual({'1': [{"title": 'дело №1', "done": False}]}, bot.data_base_lists)

    def test_delete_todo_item_answer(self):
        bot.data_base_lists = {'1': [{"title": 'дело №1', "done": False}]}
        answer, keyoard = content_text_answer('бот удали 1', '1')
        self.assertEqual('дело №1 удалено', answer)
        answer, keyoard = content_text_answer('бот удали 1', '1')
        self.assertEqual('Элемента №1 нет', answer)

    def test_delete_todo_item_base(self):
        bot.data_base_lists = {'1': [{"title": 'дело №1', "done": False}]}
        content_text_answer('бот удали 1', '1')
        self.assertEqual({}, bot.data_base_lists)

    def test_get_empty_list_answer(self):
        answer, keyoard = content_text_answer('бот покажи список', '1')
        self.assertEqual('Ваш список пока пуст', answer)

    def test_get_list_answer(self):
        bot.data_base_lists = {'1': [{"title": 'дело №1', "done": False}, {"title": 'дело №2', "done": True}]}
        answer, keyoard = content_text_answer('бот покажи список', '1')
        self.assertIn('1) дело №1', answer)
        self.assertIn('<strike>2) дело №2</strike>', answer)
        answer, keyoard = content_text_answer('бот покажи список', '2')
        self.assertIn('Ваш список пока пуст', answer)

    def test_short_commands(self):
        answer, keyoard = content_text_answer('??', '1')
        self.assertEqual('Ваш список пока пуст', answer)
        answer, keyoard = content_text_answer('++ дело №1', '1')
        self.assertEqual('дело №1 добавлено', answer)
        answer, keyoard = content_text_answer('** 1', '1')
        self.assertEqual('дело №1 зачеркнуто', answer)
        answer, keyoard = content_text_answer('-- 1', '1')
        self.assertEqual('дело №1 удалено', answer)

    def test_short_delete_todo_item_out_of_range(self):
        bot.data_base_lists = {'1': [{"title": 'дело №1', "done": False}]}
        answer, keyoard = content_text_answer('-- 2', '1')
        self.assertEqual('Элемента №2 нет', answer)
        answer, keyoard = content_text_answer('-- дело', '1')
        self.assertEqual('дело это не номер в списке', answer)

    def test_error(self):
        answer, keyoard = content_text_answer('+', '1')
        self.assertEqual('', answer)
        answer, keyoard = content_text_answer('+ дело', '1')
        self.assertEqual('', answer)
        answer, keyoard = content_text_answer('+?', '1')
        self.assertEqual('', answer)
        answer, keyoard = content_text_answer('бот добавь', '1')
        self.assertEqual('', answer)
        answer, keyoard = content_text_answer('-', '1')
        self.assertEqual('', answer)
        answer, keyoard = content_text_answer('- 1', '1')
        self.assertEqual('', answer)
        answer, keyoard = content_text_answer('-?', '1')
        self.assertEqual('', answer)
        answer, keyoard = content_text_answer('бот удали', '1')
        self.assertEqual('', answer)
        answer, keyoard = content_text_answer('бот', '1')
        self.assertEqual('', answer)

    def test_mark_item_answer(self):
        bot.data_base_lists = {'1': [{"title": 'дело №1', "done": False}]}
        answer, keyoard = content_text_answer('бот зачеркни 1', '1')
        self.assertEqual('дело №1 зачеркнуто', answer)

    def test_mark_item_base(self):
        bot.data_base_lists = {'1': [{"title": 'дело №1', "done": False}]}
        content_text_answer('бот зачеркни 1', '1')
        self.assertEqual({'1': [{"title": 'дело №1', "done": True}]}, bot.data_base_lists)
