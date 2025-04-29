from datetime import date

from database import Db
from expense import sum_expenses

CATEGORIES = ["ruoka",
              "liikenne",
              "liikunta",
              "kulttuuri",
              "sijoitukset"]


class MonthData:
    """Luokka, joka kuvastaa käyttäjän kuukauden menoja.

    Sisältää tietoa käyttäjän menoista tietyn kuukauden aikana.

    Attributes:
        expenses: Lista joka sisältää kaikki käyttäjän kuukauden menot
        total_sum: Kaikkien käyttäjän kuukauden menojen summa
        sums_by_category: Sanakirja joka sisältää jokaisen kategorian menojen
                          summan kuukauden ajalta
        daily_average: Kuukauden menojen keskiarvo päivää kohti
    """

    def __init__(self, expenses, total_sum, sums_by_category, daily_average):
        """Konstruktori, joka luo uuden MonthData-objektin.

        Args:
            expenses: Lista kaikista kuukauden menoista
            total_sum: Kuukauden menojen summa
            sums_by_category: Sanakirja joka sisältää jokaisen menokategorian
                              osalta menojen summan kuukauden ajalta
            daily_average: Keskimääräinen menojen määrä päivässä kuukauden ajalta
        """
        self.expenses = expenses
        self.total_sum = total_sum
        self.sums_by_category = sums_by_category
        self.daily_average = daily_average


class Expensetracker:
    """Luokka, joka sisältää sovelluksen logiikan.

    Attributes:
        db: Yhteys käytössä olevaan tietokataan
        user: Sisään kirjautunut käyttäjä
    """

    def __init__(self, db):
        """Luokan konstruktori, luo uuden ExpenseTrackerin.

        Args:
            db: Yhteys käytettävään tietokantaan
        """
        self.user = None
        self.db = db

    def login(self, username, passwd):
        """Yrittää kirjata käyttäjän sisään.

        Hakee käyttäjän tiedot tietokannasta ja kirjaa käyttäjän sisään jos tiedot ovat oikein.

        Args:
            username: Käyttäjänimi
            passwd: Salasana

        Returns:
            True jos sisäänkirjautuminen onnistui
            False jos käyttäjänimi tai salasana olivat väärin
        """
        user = self.db.get_user_by_username(username)
        if user and user.passwd == passwd:
            self.user = user
            return True
        return False

    def logout(self):
        """Kirjaa käyttäjän ulos"""
        self.user = None

    def create_user(self, username, passwd):
        """Luo järjestelmään uuden käyttäjän.

        Tarkastaa että käyttäjänimi ja salasana ovat riittävän pitkiä ja että käyttäjänimi
        ei ole varattu. Mikäli syötteet ovat kunnossa, luo järjestelmään uuden käyttäjän.

        Args:
            username: Käyttäjänimi (väh. 4 merkkiä)
            passwd: Salasana (väh. 4 merkkiä)

        Returns:
            True jos käyttäjän luonti onnistui
            Merkkijono joka kertoo virheen syyn mikäli käyttäjää ei voitu luoda
        """
        if len(username) < 4 or len(passwd) < 4:
            return "username or password too short"
        if not self.db.create_user(username, passwd):
            return "username already in use"
        return True

    def get_expenses(self):
        """Hakee sisään kirjautuneen käyttäjän menot.

        Returns:
            Lista joka sisältää kaikki käyttäjän kirjaamat menot
        """
        return self.db.get_expenses(self.user.user_id)

    def create_expense(self, amount, desc, category, creation_date):
        """Luo käyttäjälle uuden menon.

        Luo nykyiselle käyttäjälle uuden menon parametrien perusteella.

        Args:
            amount: Menon suuruus merkkijonona
            desc: Menon sanallinen kuvaus
            category: Menon kategoria merkkijonona
            creation_date: Menolle kirjattava aika (muodossa YYYY-MM-DD)

        Returns:
            True jos menon luonti onnistui
            False jos amount-parametri ei sisältänyt validia lukua tai jos luku oli negatiivinen
        """
        try:
            amount = format(float(amount), ".2f")
        except ValueError:
            return False
        if float(amount) < 0:
            return False
        amount_int = int(amount.split(".")[0])
        amount_dec = int(amount.split(".")[1])
        self.db.create_expense(self.user.user_id, amount_int,
                               amount_dec, desc, category, creation_date)
        return True

    def delete_expense(self, expense_id):
        """Poistaa käyttäjän menon.

        Args:
            expense_id: Poistettavan menon id
        """
        self.db.delete_expense(expense_id)

    def _calculate_daily_average(self, year, month, total_sum):
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1
        n_days = date(next_year, next_month, 1) - date(year, month, 1)
        n_days = n_days.days
        return round(total_sum / n_days, 2)

    def get_month_data(self, year, month):
        """Hakee tiedot valitusta kuukaudesta sisäänkirjautuneen käyttäjän osalta.

        Args:
            year: Valittu vuosi merkkijonona
            month: Valittu kuukausi lukuna ja merkkijonona

        Returns:
            None jos vuosi tai kuukausi ei sisältänyt numeroa tai vuosi ei ollut välillä
            [1000, 9999] tai kuukausi ei ollut välillä [1, 12], muutoin MonthData-objekti
            joka sisältää tiedot kuukauden menoista
        """
        try:
            year = int(year)
            month = int(month)
        except ValueError:
            return None
        if year < 1000 or year > 9999 or month < 1 or month > 12:
            return None
        month = "0" + str(month) if month < 9 else str(month)
        year = str(year)
        expenses = self.db.get_month_expenses(self.user.user_id, year, month)
        total_sum = sum_expenses(expenses)

        def filter_by_category(expenses, category):
            return list(filter(lambda e: e.category == category, expenses))
        expenses_by_category = {category: filter_by_category(
            expenses, category) for category in CATEGORIES}
        sums_by_category = {category: sum_expenses(
            expenses_by_category[category]) for category in CATEGORIES}
        daily_average = self._calculate_daily_average(int(year), int(month), total_sum)
        return MonthData(expenses, total_sum, sums_by_category, daily_average)


expensetracker = Expensetracker(Db())
