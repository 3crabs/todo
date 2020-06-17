import unittest

import bot
from bot import content_text_answer


class FunctionalTest(unittest.TestCase):

    def setUp(self) -> None:
        bot.data_base_subscriptions = {}

    def tearDown(self) -> None:
        bot.data_base_subscriptions = {}

    def test_open_menu(self):
        answer, keyboard = content_text_answer('бот покажи меню', '1')
        self.assertEqual(answer, 'Меню')
        self.assertIn('режим жкх', [button[0]['text'] for button in keyboard.keyboard])

    def test_add_subscription(self):
        content_text_answer('бот жкх 1-2 00:00 дело №1', '1')
        self.assertEqual(bot.data_base_subscriptions, {'1': {[
            {'label': 'дело №1',
             'start_date': '1',
             'end_date': '2',
             'time': '00:00',
             'done': False}
        ]}})
