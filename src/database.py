import sqlite3
from sqlite3 import IntegrityError
from user import User
from expense import Expense


class Db:
    def __init__(self):
        self.con = sqlite3.connect("database.db")

    def get_user_by_username(self, username):
        query = "SELECT * FROM Users WHERE username = ?"
        results = self.con.execute(query, [username]).fetchone()
        if results:
            return User(results[1], results[2], results[0])
        return None

    def create_user(self, username, passwd):
        query = "INSERT INTO Users (username, passwd) VALUES (?, ?)"
        try:
            self.con.execute(query, [username, passwd])
        except IntegrityError:
            self.con.commit()
            return False
        self.con.commit()
        return True

    def get_expenses(self, user_id):
        query = """SELECT E.amount_int, E.amount_decimal, E.date, E.desc, C.name, E.id
                   FROM Expenses E, Categories C
                   WHERE E.user_id = ? AND C.id = E.category"""
        results = self.con.execute(query, [user_id]).fetchall()
        expenses = [Expense(amount_int=x[0],
                            amount_dec=x[1],
                            date=x[2],
                            desc=x[3],
                            category=x[4],
                            expense_id=x[5]) for x in results]
        return expenses

    def create_expense(self, user_id, amount_int, amount_dec, desc, category, time):
        query = """INSERT INTO Expenses (user_id, amount_int, amount_decimal, desc, category, date)
                   VALUES (?, ?, ?, ?, ?, ?)"""
        category_query = "SELECT id FROM Categories WHERE name = ?"
        category = int(self.con.execute(
            category_query, [category]).fetchone()[0])
        self.con.execute(query, [user_id, amount_int,
                         amount_dec, desc, category, str(time)])
        self.con.commit()

    def delete_expense(self, expense_id):
        query = "DELETE FROM Expenses WHERE id = ?"
        self.con.execute(query, [expense_id])
        self.con.commit()

    def delete_all(self):
        user_query = "DELETE FROM Users"
        self.con.execute(user_query)
        expense_query = "DELETE FROM Expenses"
        self.con.execute(expense_query)
        self.con.commit()

    def get_month_expenses(self, user_id, year, month):
        search_param = f"{year}-{month}%"
        query = """SELECT E.amount_int, E.amount_decimal, E.date, E.desc, C.name, E.id
                   FROM Expenses E, Categories C
                   WHERE C.id = E.category AND user_id = ? AND date like ?"""
        results = self.con.execute(query, [user_id, search_param])
        results = [Expense(e[0], e[1], e[2], e[3], e[4], e[5])
                   for e in results]
        return results
