import sqlite3
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