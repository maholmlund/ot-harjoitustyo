class Expense:
    def __init__(self, amount_int=None, amount_dec=None, date=None,
                 desc=None, category=None, expense_id=None):
        self.amount_int = amount_int
        self.amount_dec = amount_dec
        self.date = date
        self.desc = desc
        self.category = category
        self.id = expense_id
