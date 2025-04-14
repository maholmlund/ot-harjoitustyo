from tkinter import ttk, StringVar
from expensetracker import expensetracker
from datetime import datetime


class StatsView:
    def __init__(self, root):
        self.root = root
        self.selected_month = None
        self.selected_year = None
        self.expenses = []
        self._initialize()

    def _initialize(self):
        self._frame = ttk.Frame(self.root)

        year_label = ttk.Label(self._frame, text="Year")
        year_label.grid(row=0, column=4, padx=6, pady=4)

        self.year_var = StringVar(self._frame)
        year_entry = ttk.Spinbox(
            self._frame, from_=1900, to=2100, textvariable=self.year_var)
        year_entry.grid(row=0, column=5)

        month_label = ttk.Label(self._frame, text="Month")
        month_label.grid(row=1, column=4, padx=6, pady=4)

        self.month_var = StringVar(self._frame)
        year_entry = ttk.Spinbox(
            self._frame, from_=1, to=12, textvariable=self.month_var)
        year_entry.grid(row=1, column=5)

        get_expenses_button = ttk.Button(
            self._frame, text="Get expenses", command=self._reload_expenses)
        get_expenses_button.grid(row=2, column=5, padx=6, pady=4)

        for (i, expense) in enumerate(self.expenses):
            amount = f"{expense.amount_int}.{'0' if expense.amount_dec < 10 else ''}{expense.amount_dec}€"
            amount_label = ttk.Label(self._frame, text=amount)
            amount_label.grid(row=i, column=0, padx=6, pady=4)
            desc_label = ttk.Label(self._frame, text=expense.desc)
            desc_label.grid(row=i, column=1, padx=6, pady=4)
            category_label = ttk.Label(self._frame, text=expense.category)
            category_label.grid(row=i, column=2, padx=6, pady=4)
            date_label = ttk.Label(self._frame, text=expense.date)
            date_label.grid(row=i, column=3, padx=6, pady=4)

        self._frame.pack()

    def _reload_expenses(self):
        self.year = self.year_var.get()
        self.month = self.month_var.get()
        if len(self.year) == 0:
            self.year = str(datetime.now().year)
        if len(self.month) == 0:
            self.month = str(datetime.now().month)
        if int(self.month) < 10:
            self.month = "0" + self.month
        self.expenses = expensetracker.get_month_expenses(
            self.year, self.month)
        self._frame.destroy()
        self._initialize()
