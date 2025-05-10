class Expense:
    """Luokka joka kuvastaa tietokannassa olevaa menoa.

    Attributes:
        amount_int: Kulun suuruuden kokonaisosa
        amount_dec: Kulun suuruuden desimaaliosa
        date: Kulun päivämäärä
        desc: Kulun sanallinen kuvaus
        category: Kulun kategoria
        id: Kulun id
    """

    def __init__(self, amount_int=None, amount_dec=None, date=None,
                 desc=None, category=None, expense_id=None):
        """Konstruktori, joka luo uuden kulun argumenttien perusteella.

        Args:
            amount_int: Kulun suuruuden kokonaisosa
            amount_dec: Kulun suuruuden desimaaliosa
            date: Kulun päivämäärä
            desc: Kulun sanallinen kuvaus
            category: Kulun kategoria
            expense_id: Kulun id
        """
        self.amount_int = amount_int
        self.amount_dec = amount_dec
        self.date = date
        self.desc = desc
        self.category = category
        self.id = expense_id


def sum_expenses(expenses):
    """Funktio, joka summaa yhteen listan kuluja.

    Args:
        expenses: Lista joka sisältää Expense-objekteja

    Returns:
        Kulujen summa kahden desimaalin tarkkuudella
    """
    ints = sum(e.amount_int for e in expenses)
    decs = sum(e.amount_dec for e in expenses)
    ints += decs // 100
    decs %= 100
    return ints + (decs / 100)
