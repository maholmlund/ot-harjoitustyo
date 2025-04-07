from datetime import datetime
from database import Db

CATEGORIES = ["ruoka",
              "liikenne",
              "liikunta",
              "kulttuuri",
              "sijoitukset"]

class Expensetracker:
    def __init__(self, db):
        self.user = None
        self.db = db

    def login(self, username, passwd):
        user = self.db.get_user_by_username(username)
        if user and user.passwd == passwd:
            self.user = user
            return True
        return False

    def logout(self):
        self.user = None

    def create_user(self, username, passwd):
        return self.db.create_user(username, passwd)

    def get_expenses(self):
        return self.db.get_expenses(self.user.user_id)

    def create_expense(self, amount, desc, category):
        try:
            amount = format(float(amount), ".2f")
        except ValueError:
            return False
        amount_int = int(amount.split(".")[0])
        amount_dec = int(amount.split(".")[1])
        date = datetime.now()
        self.db.create_expense(self.user.user_id, amount_int, amount_dec, desc, category, date)
        return True

expensetracker = Expensetracker(Db())
