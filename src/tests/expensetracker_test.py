import unittest
from expensetracker import Expensetracker
from user import User


class DummyDB:
    def __init__(self):
        self.data = {}

    def create_user(self, username, passwd):
        if username in self.data:
            return False
        self.data[username] = passwd

    def get_user_by_username(self, username):
        if username in self.data:
            return User(username, self.data[username], 1)
        return None


class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        self.e = Expensetracker(DummyDB())
        self.e.create_user("esimerkki", "salasana")

    def test_create_user_valid(self):
        self.assertIn("esimerkki", self.e.db.data)

    def test_create_user_short_name(self):
        self.assertTrue(type(self.e.create_user(
            "k", "salasana")) == str)
        self.assertTrue("k" not in self.e.db.data)

    def test_create_user_short_name(self):
        self.assertTrue(type(self.e.create_user(
            "liianlyhytsalasana", "123")) == str)
        self.assertTrue("k" not in self.e.db.data)

    def test_username_in_use(self):
        self.assertTrue(type(self.e.create_user(
            "esimerkki", "uusisalasana")) == str)

    def test_login_valid(self):
        self.assertTrue(self.e.login("esimerkki", "salasana"))
        self.assertTrue(self.e.user is not None)

    def test_login_invalid(self):
        self.assertFalse(self.e.login("esimerkki", "ssana"))
        self.assertTrue(self.e.user is None)

    def test_logout(self):
        self.e.logout()
        self.assertTrue(self.e.user is None)
