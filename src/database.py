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
        query = "SELECT * FROM Expenses WHERE user_id = ?"
        results = self.con.execute(query, [user_id]).fetchall()
        expenses = [Expense(x[2], x[3], x[5], x[4], x[0]) for x in results]
        return expenses
    
    def create_expense(self, user_id, amount_int, amount_dec, desc, time):
        query = "INSERT INTO Expenses (user_id, amount_int, amount_decimal, desc, date) VALUES (?, ?, ?, ?, ?)"
        self.con.execute(query, [user_id, amount_int, amount_dec, desc, str(time)])
        self.con.commit()
