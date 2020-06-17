import unittest

import bot
from bot import content_text_answer


class FunctionalTest(unittest.TestCase):

    def setUp(self) -> None:
        bot.data_base_subscriptions = {}

    def tearDown(self) -> None:
        bot.data_base_subscriptions = {}

    def test_open_menu(self):
        pass
