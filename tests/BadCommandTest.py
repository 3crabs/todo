import os
import unittest

from src.TodoBot import TodoBot


class BadCommandTest(unittest.TestCase):

    def setUp(self) -> None:
        self.bot = TodoBot("sqlite:///../static/test_todo_bot.db")

    def tearDown(self) -> None:
        os.remove("../static/test_todo_bot.db")

    def test_bad_add(self):
        answer = self.bot.message_handler('++', '1')
        self.assertEqual('', answer)

    def test_bad_delete(self):
        answer = self.bot.message_handler('--', '1')
        self.assertEqual('', answer)
        answer = self.bot.message_handler('—', '1')
        self.assertEqual('', answer)

    def test_bad_mark(self):
        answer = self.bot.message_handler('**', '1')
        self.assertEqual('', answer)
