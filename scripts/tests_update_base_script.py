import unittest

from scripts.update_base_script import update_base


class TestUpdateBase(unittest.TestCase):

    def test(self):
        db = '{' \
             '"275464432": ["\u0441\u0445\u043e\u0434\u0438\u0442\u044c \u0432 \u0442\u0443\u0430\u043b\u0435\u0442"]' \
             '}'
        new_db = '{' \
                 '"275464432": [' \
                 '{' \
                 '"title": ' \
                 '"\u0441\u0445\u043e\u0434\u0438\u0442\u044c \u0432 \u0442\u0443\u0430\u043b\u0435\u0442", ' \
                 '"done": ' \
                 'false' \
                 '}' \
                 ']' \
                 '}'
        db = update_base(db)
        self.assertEqual(new_db, db)
