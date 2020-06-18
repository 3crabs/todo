import unittest

from src.TodoBot import TodoBot


class FunctionalTest(unittest.TestCase):

    # тест на добавление элемента и просмотра списока
    def test_add_item_and_see_list(self):
        # включаем бота
        todo_bot = TodoBot()

        # добавление 'дело №1' в список
        answer, keyboard = todo_bot.content_text_answer('++ дело №1', '1')
        # 'дело №1' добавилось
        self.assertIn('дело №1', answer)
        # клавиатеры нет
        self.assertEqual(None, keyboard)

        # добавление 'дело №2' в список
        answer, keyboard = todo_bot.content_text_answer('++ дело №2', '1')
        # 'дело №2' добавилось
        self.assertIn('дело №2', answer)
        # клавиатеры нет
        self.assertEqual(None, keyboard)

        # просмотр списка
        answer, keyboard = todo_bot.content_text_answer('??', '1')
        # 'дело №1' появилось в списке под номером 1
        self.assertIn('1) дело №1', answer)
        # 'дело №2' появилось в списке под номером 2
        self.assertIn('2) дело №2', answer)
        # клавиатуры нет
        self.assertEqual(None, keyboard)

        # зачеркиваем первое дело
        answer, keyboard = todo_bot.content_text_answer('**1', '1')
        # первое дело зачеркнуто
        self.assertIn('дело №1', answer)
        # клавиатеры нет
        self.assertEqual(None, keyboard)

        # просмотр списка
        answer, keyboard = todo_bot.content_text_answer('??', '1')
        self.assertIn('<strike>1) дело №1</strike>', answer)
        self.assertIn('2) дело №2', answer)
        self.assertEqual(None, keyboard)