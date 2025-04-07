from tkinter import ttk, StringVar
from expensetracker import expensetracker, CATEGORIES

class MainView:
    def __init__(self, root, handle_logout):
        self.root = root
        self.handle_logout = handle_logout
        self.error_msg = None
        self._initialize()
    
    def _initialize(self):
        self._frame = ttk.Frame(self.root)
        logout_button = ttk.Button(self._frame, text="Log out", command=self._logout)
        logout_button.grid(row=0, column=5, padx=6, pady=4)

        sum_label = ttk.Label(self._frame, text="Sum:")
        sum_label.grid(row=1, column=3, padx=6, pady=4)

        desc_label = ttk.Label(self._frame, text="Description")
        desc_label.grid(row=2, column=3, padx=6, pady=4)

        self.sum_var = StringVar(self._frame)
        sum_field = ttk.Entry(self._frame, textvariable=self.sum_var)
        sum_field.grid(row=1, column=5, padx=6, pady=4)

        self.desc_var = StringVar(self._frame)
        desc_field = ttk.Entry(self._frame, textvariable=self.desc_var)
        desc_field.grid(row=2, column=5, padx=6, pady=4)

        self.category_var = StringVar(self._frame)
        category_field = ttk.OptionMenu(self._frame, self.category_var, *CATEGORIES)
        category_field.grid(row=3, column=5, padx=6, pady=4)

        create_button = ttk.Button(self._frame, text="Create", command=self._create_expense)
        create_button.grid(row=4, column=4, columnspan=2, padx=6, pady=4)

        if self.error_msg:
            error_msg = ttk.Label(self._frame, text=self.error_msg, foreground="red")
            error_msg.grid(row=5, column=4, columnspan=2, padx=6, pady=4)

        expenses = expensetracker.get_expenses()
        for (i, expense) in enumerate(expenses):
            amount = f"{expense.amount_int}.{"0" if expense.amount_dec < 10 else ""}{expense.amount_dec}€"
            amount_label = ttk.Label(self._frame, text=amount)
            amount_label.grid(row=i, column=0, padx=6, pady=4)
            desc_label = ttk.Label(self._frame, text=expense.desc)
            desc_label.grid(row=i, column=1, padx=6, pady=4)
            category_label = ttk.Label(self._frame, text=expense.category)
            category_label.grid(row=i, column=2, padx=6, pady=4)
        
        self._frame.pack()
        
    def _create_expense(self):
        self.error_msg = None
        sum_value = self.sum_var.get()
        desc = self.desc_var.get()
        category = self.category_var.get()
        if not expensetracker.create_expense(sum_value, desc, category):
            self.error_msg = "invalid number format"
        self._frame.destroy()
        self._initialize()

    def _logout(self):
        expensetracker.logout()
        self._frame.destroy()
        self.handle_logout(self.root, MainView)
