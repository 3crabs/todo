import unittest

from src.Chat import Chat
from src.ListItem import ListItem
from src.TodoBot import TodoBot


class FunctionalTest(unittest.TestCase):

    def test_add_item(self):
        todo_bot = TodoBot()
        todo_list = ['дело №1', 'дело №2']
        for item in todo_list:
            answer, keyboard = todo_bot.content_text_answer(f'++ {item}', '1')
            self.assertIn(item, answer)
            self.assertEqual(None, keyboard)

    def test_add_item_check_base(self):
        todo_bot = TodoBot()
        todo_list = ['дело №1', 'дело №2']
        for item in todo_list:
            todo_bot.content_text_answer(f'++ {item}', '1')
            self.assertIn(item, [item.label for item in todo_bot.get_chat_by_id('1').chat_list])

    def test_see_list(self):
        todo_bot = TodoBot()
        todo_bot.chats = [Chat('1', [ListItem('дело №1', 'strike'), ListItem('дело №2')])]
        answer, keyboard = todo_bot.content_text_answer('??', '1')
        self.assertIn('<strike>1) дело №1</strike>', answer)
        self.assertIn('2) дело №2', answer)
        self.assertEqual(None, keyboard)

    def test_see_empty_list(self):
        todo_bot = TodoBot()
        answer, keyboard = todo_bot.content_text_answer('??', '1')
        self.assertIn('Список пуст', answer)
        self.assertEqual(None, keyboard)

    def test_strike_item(self):
        todo_bot = TodoBot()
        todo_bot.chats = [Chat('1', [ListItem('дело №1'), ListItem('дело №2')])]
        answer, keyboard = todo_bot.content_text_answer('**1', '1')
        self.assertIn('дело №1', answer)
        self.assertEqual(None, keyboard)
        answer, keyboard = todo_bot.content_text_answer('**2', '1')
        self.assertIn('дело №2', answer)
        self.assertEqual(None, keyboard)

    def test_strike_item_check_base(self):
        todo_bot = TodoBot()
        todo_bot.chats = [Chat('1', [ListItem('дело №1'), ListItem('дело №2')])]
        todo_bot.content_text_answer('**1', '1')
        self.assertEqual(['strike', 'none'], [item.state for item in todo_bot.get_chat_by_id('1').chat_list])
        todo_bot.content_text_answer('**2', '1')
        self.assertEqual(['strike', 'strike'], [item.state for item in todo_bot.get_chat_by_id('1').chat_list])

    def test_delete_item(self):
        todo_bot = TodoBot()
        todo_bot.chats = [Chat('1', [ListItem('дело №1'), ListItem('дело №2')])]
        answer, keyboard = todo_bot.content_text_answer('--1', '1')
        self.assertIn('дело №1', answer)
        self.assertEqual(None, keyboard)

    def test_delete_item_check_base(self):
        todo_bot = TodoBot()
        todo_bot.chats = [Chat('1', [ListItem('дело №1'), ListItem('дело №2')])]
        todo_bot.content_text_answer('--1', '1')
        self.assertNotIn('дело №1', [item.label for item in todo_bot.get_chat_by_id('1').chat_list])

    def test_delete_all_strike_items(self):
        todo_bot = TodoBot()
        todo_bot.chats = [Chat('1', [ListItem('дело №1', 'strike')])]
        answer, keyboard = todo_bot.content_text_answer('---', '1')
        self.assertEqual('Все зачеркнутые дела удалены', answer)
        self.assertEqual(None, keyboard)

    def test_delete_all_strike_items_check_base(self):
        todo_bot = TodoBot()
        todo_bot.chats = [Chat('1', [ListItem('дело №1', 'strike')])]
        todo_bot.content_text_answer('---', '1')
        self.assertNotIn('strike', [item.state for item in todo_bot.get_chat_by_id('1').chat_list])
