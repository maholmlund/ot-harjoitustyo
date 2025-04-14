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
        if len(username) < 4 or len(passwd) < 4:
            return "username or password too short"
        if not self.db.create_user(username, passwd):
            return "username already in use"
        return True

    def get_expenses(self):
        return self.db.get_expenses(self.user.user_id)

    def create_expense(self, amount, desc, category, date):
        try:
            amount = format(float(amount), ".2f")
        except ValueError:
            return False
        if float(amount) < 0:
            return False
        amount_int = int(amount.split(".")[0])
        amount_dec = int(amount.split(".")[1])
        self.db.create_expense(self.user.user_id, amount_int,
                               amount_dec, desc, category, date)
        return True

    def get_month_expenses(self, year, month):
        return self.db.get_month_expenses(year, month)

    def get_month_expenses_total(self, year, month):
        expenses = self.get_month_expenses(year, month)
        sum_int = sum(e.amount_int for e in expenses)
        sum_dec = sum(e.amount_dec for e in expenses)
        sum_int += sum_dec // 100
        result = sum_int + (sum_dec / 100)
        return result


expensetracker = Expensetracker(Db())
