import unittest

from src.TodoBot import TodoBot


class FunctionalTest(unittest.TestCase):

    # тест на добавление элемента и просмотра списока
    def test_add_item_and_see_list(self):
        # включаем бота
        todo_bot = TodoBot()

        # просмотр списка
        answer, keyboard = todo_bot.content_text_answer('??', '1')
        self.assertIn('Список пуст', answer)
        self.assertEqual(None, keyboard)

        # добавление 'дело №1' в список
        answer, keyboard = todo_bot.content_text_answer('++ дело №1', '1')
        self.assertIn('дело №1', answer)
        self.assertEqual(None, keyboard)

        # добавление 'дело №2' в список
        answer, keyboard = todo_bot.content_text_answer('++ дело №2', '1')
        self.assertIn('дело №2', answer)
        self.assertEqual(None, keyboard)

        # просмотр списка
        answer, keyboard = todo_bot.content_text_answer('??', '1')
        self.assertIn('1) дело №1', answer)
        self.assertIn('2) дело №2', answer)
        self.assertEqual(None, keyboard)

        # зачеркиваем первое дело
        answer, keyboard = todo_bot.content_text_answer('**1', '1')
        self.assertIn('дело №1', answer)
        self.assertEqual(None, keyboard)

        # просмотр списка
        answer, keyboard = todo_bot.content_text_answer('??', '1')
        self.assertIn('<strike>1) дело №1</strike>', answer)
        self.assertIn('2) дело №2', answer)
        self.assertEqual(None, keyboard)