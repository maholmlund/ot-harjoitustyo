import unittest
from expensetracker import Expensetracker
from user import User
from expense import Expense


class DummyDB:
    def __init__(self):
        self.users = {}
        self.expenses = []

    def create_user(self, username, passwd):
        if username in self.users:
            return False
        self.users[username] = passwd
        return True

    def get_user_by_username(self, username):
        if username in self.users:
            return User(username, self.users[username], 1)
        return None

    def create_expense(self, user_id, amount_int, amount_dec, desc, category, time):
        self.expenses.append(
            Expense(amount_int, amount_dec, time, desc, category, 1))

    def get_expenses(self, user_id):
        return self.expenses

    def get_month_expenses(self, year, month):
        date_start = f"{year}-{month}"
        return list(filter(lambda e: e.date.startswith(date_start), self.expenses))


class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        self.e = Expensetracker(DummyDB())
        self.e.create_user("esimerkki", "salasana")

    def test_create_user_valid(self):
        self.assertIn("esimerkki", self.e.db.users)

    def test_create_user_short_name(self):
        self.assertTrue(type(self.e.create_user(
            "k", "salasana")) == str)
        self.assertTrue("k" not in self.e.db.users)

    def test_create_user_short_name(self):
        self.assertTrue(type(self.e.create_user(
            "liianlyhytsalasana", "123")) == str)
        self.assertTrue("k" not in self.e.db.users)

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

    def test_create_expense_valid(self):
        self.e.login("esimerkki", "salasana")
        self.e.create_expense("23.23", "ostoksia", "ruoka", "2025-11")
        self.assertEqual(len(self.e.get_expenses()), 1)

    def test_create_expense_negative(self):
        self.e.login("esimerkki", "salasana")
        self.assertFalse(self.e.create_expense(
            "-1", "ostoksia", "ruoka", "2025-11"))

    def test_create_expense_invalid_number(self):
        self.e.login("esimerkki", "salasana")
        self.assertFalse(self.e.create_expense(
            "python", "ostoksia", "ruoka", "2025-11"))

    def test_get_month_expenses_total(self):
        self.e.login("esimerkki", "salasana")
        self.e.create_expense("32.11", "jotain lisää",
                              "sijoitukset", "2025-04")
        self.e.create_expense("1.1", "halpa ostos",
                              "ruoka", "2025-04")
        self.assertEqual(self.e.get_month_expenses_total("2025", "04"), 33.21)
