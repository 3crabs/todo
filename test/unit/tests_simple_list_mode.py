import unittest

from src.TodoBot import TodoBot


class FunctionalTest(unittest.TestCase):

    def test_add_item(self):
        todo_bot = TodoBot()
        todo_list = ['дело №1', 'дело №2', 'дело №3']
        for item in todo_list:
            answer, keyboard = todo_bot.content_text_answer(f'++ {item}', '1')
            self.assertIn(item, answer)
            self.assertEqual(None, keyboard)

    def test_add_item_1_check_base(self):
        todo_bot = TodoBot()
        todo_list = ['дело №1', 'дело №2', 'дело №3']
        for item in todo_list:
            todo_bot.content_text_answer(f'++ {item}', '1')
            self.assertIn(item, [item['label'] for item in todo_bot.get_list('1')])

    def test_see_list(self):
        todo_bot = TodoBot()
        todo_bot.lists = {'1': {'list': [
            {'label': 'дело №1', 'state': 'none'},
            {'label': 'дело №2', 'state': 'none'},
        ]}}
        answer, keyboard = todo_bot.content_text_answer('??', '1')
        self.assertIn('1) дело №1', answer)
        self.assertIn('2) дело №2', answer)
        self.assertEqual(None, keyboard)
