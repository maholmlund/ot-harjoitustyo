from tkinter import ttk, StringVar
from expensetracker import expensetracker

class MainView:
    def __init__(self, root):
        self.root = root
        self._initialize()
    
    def _initialize(self):
        logout_button = ttk.Button(self.root, text="Log out")
        logout_button.grid(row=0, column=3, padx=6, pady=4)

        sum_label = ttk.Label(self.root, text="Sum:")
        sum_label.grid(row=1, column=2, padx=6, pady=4)

        desc_label = ttk.Label(self.root, text="Description")
        desc_label.grid(row=2, column=2, padx=6, pady=4)

        self.sum_var = StringVar(self.root)
        sum_field = ttk.Entry(self.root, textvariable=self.sum_var)
        sum_field.grid(row=1, column=3, padx=6, pady=4)

        self.desc_var = StringVar(self.root)
        desc_field = ttk.Entry(self.root, textvariable=self.desc_var)
        desc_field.grid(row=2, column=3, padx=6, pady=4)

        create_button = ttk.Button(self.root, text="Create", command=self._create_expense)
        create_button.grid(row=3, column=2, columnspan=2, padx=6, pady=4)

        expenses = expensetracker.get_expenses()
        for (i, expense) in enumerate(expenses):
            text = f"{expense.amount_int}.{expense.amount_dec}€ {expense.desc}"
            label = ttk.Label(self.root, text=text)
            label.grid(row=i, column=0, padx=6, pady=4)
        
    def _create_expense(self):
        sum_value = self.sum_var.get()
        desc = self.desc_var.get()
        expensetracker.create_expense(float(sum_value), desc)