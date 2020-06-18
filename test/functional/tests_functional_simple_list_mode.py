import unittest

from src.TodoBot import TodoBot


class FunctionalTest(unittest.TestCase):

    # тест на добавление элемента и просмотра списока
    def test_add_item_and_see_list(self):
        # включаем бота
        todo_bot = TodoBot()

        # добавление 'дело №1' в список
        answer, keyboard = todo_bot.content_text_answer('++ дело №1', '1')

        # 'дело №1' появилось в списке под номером 1
        self.assertIn('дело №1', answer)
        # клавиатеры нет
        self.assertEqual(None, keyboard)

        # просмотр списка
        answer, keyboard = todo_bot.content_text_answer('??', '1')

        # 'дело №1' появилось в списке под номером 1
        self.assertIn('1) дело №1', answer)
        # клавиатеры нет
        self.assertEqual(None, keyboard)
