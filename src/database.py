import sqlite3
from sqlite3 import IntegrityError
from user import User

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
