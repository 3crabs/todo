import unittest

from src.TodoBot import TodoBot


class FunctionalTest(unittest.TestCase):

    def test_add_item(self):
        todo_bot = TodoBot()
        answer, keyboard = todo_bot.content_text_answer('++ дело №1', '1')
        self.assertIn('дело №1', answer)
        self.assertEqual(None, keyboard)

    def test_see_list(self):
        todo_bot = TodoBot()
        answer, keyboard = todo_bot.content_text_answer('??', '1')
        self.assertIn('1) дело №1', answer)
        self.assertEqual(None, keyboard)
