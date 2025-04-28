from database import Db
from expense import sum_expenses

CATEGORIES = ["ruoka",
              "liikenne",
              "liikunta",
              "kulttuuri",
              "sijoitukset"]


class MonthData:
    def __init__(self, expenses, total_sum, sums_by_category):
        self.expenses = expenses
        self.total_sum = total_sum
        self.sums_by_category = sums_by_category


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

    def get_month_data(self, year, month):
        try:
            year = int(year)
            month = int(month)
        except ValueError:
            return None
        if year < 1000 or year > 9999 or month < 1 or month > 12:
            return None
        month = "0" + str(month) if month < 9 else str(month)
        year = str(year)
        expenses = self.db.get_month_expenses(self.user.user_id, year, month)
        total_sum = sum_expenses(expenses)

        def filter_by_category(expenses, category):
            return list(filter(lambda e: e.category == category, expenses))
        expenses_by_category = {category: filter_by_category(
            expenses, category) for category in CATEGORIES}
        sums_by_category = {category: sum_expenses(
            expenses_by_category[category]) for category in CATEGORIES}
        return MonthData(expenses, total_sum, sums_by_category)


expensetracker = Expensetracker(Db())
