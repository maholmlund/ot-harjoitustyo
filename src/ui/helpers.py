from tkinter import ttk
from expensetracker import expensetracker
from config import CONFIG


def build_expense_table(frame, start_row, start_col, expenses, after_delete):
    """Funktio, joka luo ikkunaan menoja kuvaavan taulukon.

    Args:
        frame: Frame johon taulukko luodaan
        start_row: Taulukon ensimmäisen rivin indeksi
        start_col: Taulukon ensimmäisen sarakkeen indeksi
        expenses: Taulukkoon halutut menot listana Expense-objekteja
        after_delete: Funktio, joka kutsutaan käyttäjän poistettua menon Delete-painikkeella
    """
    for (i, expense) in enumerate(expenses):
        i += start_row
        amount = f"{expense.amount_int}.{'0' if expense.amount_dec < 10 else ''}{expense.amount_dec}{CONFIG['currency']}"
        amount_label = ttk.Label(frame, text=amount)
        amount_label.grid(row=i, column=start_col, padx=6, pady=4)
        desc_label = ttk.Label(frame, text=expense.desc)
        desc_label.grid(row=i, column=start_col + 1, padx=6, pady=4)
        category_label = ttk.Label(frame, text=expense.category)
        category_label.grid(row=i, column=start_col + 2, padx=6, pady=4)
        date_label = ttk.Label(frame, text=expense.date)
        date_label.grid(row=i, column=start_col + 3, padx=6, pady=4)
        delete_button = ttk.Button(frame, text="Delete", command=_delete_expense(
            expense.id, after_delete=after_delete))
        delete_button.grid(row=i, column=start_col + 4, padx=6, pady=4)


def _delete_expense(expense_id, after_delete):
    def func():
        expensetracker.delete_expense(expense_id)
        after_delete()
    return func
