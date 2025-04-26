from tkinter import ttk


def build_expense_table(frame, start_row, start_col, expenses):
    for (i, expense) in enumerate(expenses):
        i += start_row
        amount = f"{expense.amount_int}.{'0' if expense.amount_dec < 10 else ''}{expense.amount_dec}€"
        amount_label = ttk.Label(frame, text=amount)
        amount_label.grid(row=i, column=start_col, padx=6, pady=4)
        desc_label = ttk.Label(frame, text=expense.desc)
        desc_label.grid(row=i, column=start_col + 1, padx=6, pady=4)
        category_label = ttk.Label(frame, text=expense.category)
        category_label.grid(row=i, column=start_col + 2, padx=6, pady=4)
        date_label = ttk.Label(frame, text=expense.date)
        date_label.grid(row=i, column=start_col + 3, padx=6, pady=4)
