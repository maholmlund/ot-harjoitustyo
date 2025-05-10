from tkinter import ttk, StringVar
from expensetracker import expensetracker
from datetime import datetime

from config import CONFIG
from ui.helpers import build_expense_table


class StatsView:
    """Kuukausittaisen statistiikan näyttämisestä vastaava luokka."""

    def __init__(self, root, reload_all_windows):
        """Konstruktori, joka luo uuden statistiikkanäkymän.

        Args:
            root: Uuden framen juuri
            reload_all_windows: Funktio, joka kutsuttaessa lataa uudelleen kaikki
                                ikkunat (tarvitaan, jos käyttäjä poistaa menon 
                                statistiikkanäkymästä)
        """
        self._root = root
        self._reload_all_windows = reload_all_windows
        self._frame = ttk.Frame(self._root)
        self._year_var = StringVar(self._frame)
        self._month_var = StringVar(self._frame)
        self._month_data = None
        self.reload_window()

    def _initialize(self):

        year_label = ttk.Label(self._frame, text="Year")
        year_entry = ttk.Spinbox(self._frame, from_=1900, to=2100, textvariable=self._year_var)
        month_label = ttk.Label(self._frame, text="Month")
        month_entry = ttk.Spinbox(self._frame, from_=1, to=12, textvariable=self._month_var)
        get_expenses_button = ttk.Button(
            self._frame, text="Get expenses", command=self.reload_window)
        total_label = ttk.Label(
            self._frame, text=f"Total this month: {self._month_data.total_sum}{CONFIG['currency']}")
        average_label = ttk.Label(
            self._frame, text=f"Daily average: {self._month_data.daily_average}{CONFIG['currency']}/day")
        date_label = ttk.Label(
            self._frame, text=f"Expenses for {self._month_var.get()}/{self._year_var.get()}")
        category_label = ttk.Label(self._frame, text="Total sum by category:")

        year_label.grid(row=0, column=5, padx=6, pady=4)
        year_entry.grid(row=0, column=6)
        month_label.grid(row=1, column=5, padx=6, pady=4)
        month_entry.grid(row=1, column=6, padx=6, pady=4)
        get_expenses_button.grid(row=2, column=6, padx=6, pady=4)
        total_label.grid(row=4, column=5, columnspan=2, padx=6, pady=4)
        average_label.grid(row=5, column=5, columnspan=2, padx=6, pady=4)
        date_label.grid(row=0, column=0, padx=6, pady=4, columnspan=4)
        category_label.grid(row=6, column=5, columnspan=2, padx=6, pady=4)

        build_expense_table(self._frame, 1, 0, self._month_data.expenses, self._reload_all_windows)
        self._build_category_sum_list(7, 5)

        self._frame.pack()

    def _build_category_sum_list(self, start_row, start_col):
        for row, category in enumerate(CONFIG["categories"]):
            category_label = ttk.Label(self._frame, text=category)
            sum_label = ttk.Label(
                self._frame, text=f"{self._month_data.sums_by_category[category]}{CONFIG['currency']}")
            category_label.grid(row=start_row + row, column=start_col, padx=6, pady=4)
            sum_label.grid(row=start_row + row, column=start_col + 1, padx=6, pady=4)

    def reload_window(self):
        """Lataa uudelleen statistiikkaikkunan."""
        self._reload_expenses()
        self._frame.destroy()
        self._frame = ttk.Frame(self._root)
        self._initialize()

    def _reload_expenses(self):
        year = self._year_var.get()
        month = self._month_var.get()
        self._month_data = expensetracker.get_month_data(year, month)
        if self._month_data is None:
            year = str(datetime.now().year)
            month = str(datetime.now().month)
            self._month_data = expensetracker.get_month_data(year, month)
        self._year_var.set(year)
        self._month_var.set(month)
