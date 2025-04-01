import unittest
from expensetracker import Expensetracker

class DummyDB:
    def __init__(self):
        self.data = {}
    
    def create_user(self, username, passwd):
        self.data[username] = passwd

class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        self.e = Expensetracker(DummyDB())
    
    def test_create_user(self):
        self.e.create_user("esimerkki", "salasana")
        self.assertIn("esimerkki", self.e.db.data)