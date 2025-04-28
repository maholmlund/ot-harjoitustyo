import unittest
import time
from database import Db


class TestDataBase(unittest.TestCase):
    def setUp(self):
        self.db = Db()
        self.db.delete_all()
        self.db.create_user("testi", "salasana")

    def test_create_user(self):
        self.assertTrue(self.db.create_user("tarmo", "salasana"))
        user = self.db.get_user_by_username("tarmo")
        self.assertIsNotNone(user)

    def test_create_invalid_user(self):
        self.assertFalse(self.db.create_user("testi", "salasana2"))

    def test_get_invalid_user(self):
        self.assertIsNone(self.db.get_user_by_username("nonexistent"))

    def test_create_expense(self):
        self.db.create_expense(1, 3, 3, "something", "ruoka", time.time())
        self.assertEqual(len(self.db.get_expenses(1)), 1)

    def test_get_month_expenses(self):
        self.db.create_expense(1, 3, 3, "something", "ruoka", "2025-04-28")
        self.db.create_expense(1, 3, 3, "something", "ruoka", "2025-04-28")
        self.assertEqual(len(self.db.get_month_expenses(1, "2025", "04")), 2)
