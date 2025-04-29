import unittest
from expense import Expense, sum_expenses


class TestExpense(unittest.TestCase):
    def setUp(self):
        self.expenses = []
        self.expenses.append(Expense(2, 23, "2025-04-29", "jotain", "ruoka", 1))
        self.expenses.append(Expense(10, 0, "2025-04-29", "lisää jotain", "ruoka", 2))
        self.expenses.append(Expense(99999999, 99, "2025-04-29", "ökyjahti", "liikenne", 3))

    def test_sum_expenses(self):
        result = sum_expenses(self.expenses)
        self.assertEqual(result, 100000012.22)
