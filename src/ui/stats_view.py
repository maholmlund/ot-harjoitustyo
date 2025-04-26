from tkinter import ttk, StringVar
from expensetracker import expensetracker
from datetime import datetime

from ui.helpers import build_expense_table


class StatsView:
    def __init__(self, root):
        self._root = root
        self._selected_month = None
        self._selected_year = None
        self._expenses = []
        self._sum_total = 0
        self._frame = ttk.Frame(self._root)
        self._initialize()
        self._reload_expenses()

    def _initialize(self):

        self.year_var = StringVar(self._frame)
        self.month_var = StringVar(self._frame)

        year_label = ttk.Label(self._frame, text="Year")
        year_entry = ttk.Spinbox(self._frame, from_=1900, to=2100, textvariable=self.year_var)
        month_label = ttk.Label(self._frame, text="Month")
        month_entry = ttk.Spinbox(self._frame, from_=1, to=12, textvariable=self.month_var)
        get_expenses_button = ttk.Button(self._frame, text="Get expenses", command=self._reload_expenses)
        total_label = ttk.Label(self._frame, text=f"Total this month: {self._sum_total}€")
        date_label = ttk.Label(self._frame, text=f"Expenses for {self._selected_month}/{self._selected_year}")

        year_label.grid(row=0, column=4, padx=6, pady=4)
        year_entry.grid(row=0, column=5)
        month_label.grid(row=1, column=4, padx=6, pady=4)
        month_entry.grid(row=1, column=5, padx=6, pady=4)
        get_expenses_button.grid(row=2, column=5, padx=6, pady=4)
        total_label.grid(row=3, column=5, padx=6, pady=4)
        date_label.grid(row=0, column=0, padx=6, pady=4, columnspan=4)

        build_expense_table(self._frame, 1, 0, self._expenses)

        self._frame.pack()

    def _reload_expenses(self):
        self._selected_year = self.year_var.get()
        self._selected_month = self.month_var.get()
        try:
            int(self._selected_year)
        except ValueError:
            self._selected_year = str(datetime.now().year)
        try:
            int(self._selected_month)
        except ValueError:
            self._selected_month = str(datetime.now().month)
        if int(self._selected_month) < 10:
            self._selected_month = "0" + self._selected_month
        self._expenses = expensetracker.get_month_expenses(self._selected_year, self._selected_month)
        self._sum_total = expensetracker.get_month_expenses_total(self._selected_year, self._selected_month)
        self._frame.destroy()
        self._frame = ttk.Frame(self._root)
        self._initialize()
