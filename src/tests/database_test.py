import unittest
import time
import os
from sqlite3 import connect
from database import Db, init_db_file
from config import CONFIG


class TestDataBase(unittest.TestCase):
    def setUp(self):
        CONFIG["dbfile"] = ".testdb.db"
        CONFIG["categories"] = ["ruoka"]
        os.remove(".testdb.db")
        self.db = Db()
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

    def test_delete_expense(self):
        self.db.create_expense(1, 3, 3, "something", "ruoka", time.time())
        self.db.delete_expense(1)
        self.assertEqual(len(self.db.get_expenses(1)), 0)

    def test_get_month_expenses(self):
        self.db.create_expense(1, 3, 3, "something", "ruoka", "2025-04-28")
        self.db.create_expense(1, 3, 3, "something", "ruoka", "2025-04-28")
        self.assertEqual(len(self.db.get_month_expenses(1, "2025", "04")), 2)

    def test_init_db_file(self):
        os.remove(".testdb.db")
        init_db_file()
        # this should crash if the file is not correctly initialized
        self.db = Db()
        self.db.create_user("testi", "salasana")
        self.db.create_expense(1, 3, 3, "something", "ruoka", "2025-04-28")

    def test_constructor_invalid_db(self):
        # create database with missing tables
        os.remove(".testdb.db")
        con = connect(".testdb.db")
        con.execute("CREATE TABLE Users (id INTEGER, name TEXT)")
        con.commit()

        self.db = Db()

        # this should crash if the file is not correctly initialized
        self.db.create_user("testi", "salasana")
        self.db.create_expense(1, 3, 3, "something", "ruoka", "2025-04-28")

    def test_constructor_missing_file(self):
        os.remove(".testdb.db")
        # this should not crash
        self.db = Db()

    def test_update_categories(self):
        CONFIG["categories"] = ["yksi", "kaksi"]
        self.db = Db()
        CONFIG["categories"] = ["kaksi", "kolme"]
        self.db = Db()
        query = "SELECT name FROM Categories"
        con = connect(".testdb.db")
        categories = [x[0] for x in con.execute(query)]
        self.assertEqual(categories, ["kaksi", "kolme"])
