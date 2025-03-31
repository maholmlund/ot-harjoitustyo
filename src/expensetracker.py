from database import Db

class Expensetracker:
    def __init__(self):
        self.user = None

    def login(self, username, passwd):
        user = Db().get_user_by_username(username)
        if user and user.passwd == passwd:
            self.user = user
            return True
        return False
    
    def create_user(self, username, passwd):
        return Db().create_user(username, passwd)

expensetracker = Expensetracker()
