from tkinter import ttk, StringVar, Toplevel
from expensetracker import expensetracker, CATEGORIES
from tkcalendar import DateEntry
from ui.stats_view import StatsView
from ui.helpers import build_expense_table


class MainView:
    def __init__(self, root, handle_logout):
        self.root = root
        self.handle_logout = handle_logout
        self.error_msg = None
        self.stats_window = None
        self.stats_view = None
        self._frame = ttk.Frame(self.root)
        self._initialize()

    def _initialize(self):
        logout_button = ttk.Button(self._frame, text="Log out", command=self._logout)
        logout_button.grid(row=0, column=6, padx=6, pady=4)

        self.sum_var = StringVar(self._frame)
        self.desc_var = StringVar(self._frame)
        self.category_var = StringVar(self._frame)
        self.date_var = StringVar(self._frame)

        if self.error_msg:
            error_msg = ttk.Label(self._frame, text=self.error_msg, foreground="red")
            error_msg.grid(row=6, column=6, columnspan=2, padx=6, pady=4)

        stats_button = ttk.Button(self._frame, text="Monthly stats",
                                  command=self._show_monthly_view)
        stats_button.grid(row=7, column=6, columnspan=2, padx=6, pady=4)

        build_expense_table(self._frame, 0, 0, expensetracker.get_expenses(), self._reload_window)
        self._build_new_expense_controls(1, 5)
        self._frame.pack()

    def _build_new_expense_controls(self, start_row, start_col):
        sum_label = ttk.Label(self._frame, text="Sum:")
        desc_label = ttk.Label(self._frame, text="Description")
        sum_field = ttk.Entry(self._frame, textvariable=self.sum_var)
        desc_field = ttk.Entry(self._frame, textvariable=self.desc_var)
        category_field = ttk.OptionMenu(self._frame, self.category_var, *CATEGORIES)
        date_field = DateEntry(self._frame, textvariable=self.date_var, date_pattern="yyyy-mm-dd")
        create_button = ttk.Button(self._frame, text="Create", command=self._create_expense)

        sum_label.grid(row=start_row, column=start_col, padx=6, pady=4)
        desc_label.grid(row=start_row + 1, column=start_col, padx=6, pady=4)
        sum_field.grid(row=start_row, column=start_col + 1, padx=6, pady=4)
        desc_field.grid(row=start_row + 1, column=start_col + 1, padx=6, pady=4)
        category_field.grid(row=start_row + 2, column=start_col + 1, padx=6, pady=4)
        date_field.grid(row=start_row + 3, column=start_col + 1, padx=6, pady=4)
        create_button.grid(row=start_row + 4, column=start_col + 1, columnspan=2, padx=6, pady=4)

    def _reload_window(self):
        self._frame.destroy()
        self._frame = ttk.Frame(self.root)
        self._initialize()

    def _create_expense(self):
        self.error_msg = None
        sum_value = self.sum_var.get()
        desc = self.desc_var.get()
        category = self.category_var.get()
        date = self.date_var.get()
        if not expensetracker.create_expense(sum_value, desc, category, date):
            self.error_msg = "invalid number format"
        self._reload_window()

    def _logout(self):
        expensetracker.logout()
        self._frame.destroy()
        self.handle_logout(self.root, MainView)

    def _show_monthly_view(self):
        if self.stats_window is not None:
            self._on_stats_close()
        else:
            self.stats_window = Toplevel(self.root)
            self.stats_window.protocol("WM_DELETE_WINDOW", self._on_stats_close)
            self.stats_view = StatsView(self.stats_window)

    def _on_stats_close(self):
        self.stats_window.destroy()
        self.stats_window = None
        self.stats_view = None
