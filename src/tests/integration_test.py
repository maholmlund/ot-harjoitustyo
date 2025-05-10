from config import CONFIG
from expensetracker import Expensetracker
from database import Db

import os
import unittest


class TestIntegration(unittest.TestCase):
    def setUp(self):
        if os.path.isfile(".testdb.db"):
            os.remove(".testdb.db")
        CONFIG["dbfile"] = ".testdb.db"
        CONFIG["categories"] = ["ruoka", "vaatteet", "muut"]
        self.e = Expensetracker(Db())
        self.e.create_user("mikko", "mallikas")
        self.e.login("mikko", "mallikas")
        self.assertTrue(self.e.create_expense("22.22", "jotain", "ruoka", "2025-05-10"))
        self.assertEqual(len(self.e.get_expenses()), 1)
        self.assertIsNotNone(self.e.user)

    def test_get_month_data_valid(self):
        self.e.create_expense("1.1", "halpaa", "ruoka", "2025-05-10")
        self.e.create_expense("999", "kallis osake", "muut", "2025-05-10")
        self.e.create_expense("30", "t-paita", "vaatteet", "2025-04-10")
        data = self.e.get_month_data("2025", "5")
        self.assertEqual(data.sums_by_category["ruoka"], 23.32)
        self.assertEqual(data.daily_average, 32.98)

    def test_get_month_data_invalid_month(self):
        self.assertIsNone(self.e.get_month_data("2025", "15"))

    def test_delete_expense(self):
        self.e.delete_expense(1)
        self.assertEqual(len(self.e.get_expenses()), 0)

    def test_logout(self):
        self.e.logout()
        self.assertIsNone(self.e.user)
