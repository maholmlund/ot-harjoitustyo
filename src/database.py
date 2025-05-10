import sqlite3
from sqlite3 import IntegrityError, OperationalError
import os

from user import User
from expense import Expense
from config import CONFIG


def init_db_file():
    """Funktio, joka luo uuden tietokantatiedoston tiedostoon trackerconf.toml.

    Poistaa aiemman tiedoston ja alustaa tietokannan schema.sql-tiedoston mukaan.
    """
    try:
        os.remove(CONFIG["dbfile"])
    except FileNotFoundError:
        pass
    # a nice shell injection :)
    os.system(f"cat src/schema.sql | sqlite3 {CONFIG['dbfile']}")
    con = sqlite3.connect(CONFIG["dbfile"])
    for c in CONFIG["categories"]:
        con.execute("INSERT INTO Categories (name) VALUES (?)", [c])
    con.commit()


class Db:
    """Luokka, joka mahdollistaa tietokannan käytön."""

    def __init__(self):
        """Konstruktori, joka luo uuden yhteyden tietokantaan.

        Mikäli tiedostoa ei ole olemassa tai se ei ole validi, alustaa tietokannan.
        Jos konfiguraatiossa on määritelty eri kategoriat kuin mitä tietokannassa sillä
        hetkellä on, päivittää kategoriat tietokantaan vastaamaan konfiguraatiota.

        Huom! Mikäli
        jokin kategoria ei ole konfiguraatiossa mutta on tietokannassa, poistetaan se
        tietokannasta, samoin kaikki tähän kategoriaan luokitellut menot.
        """
        if not self._file_is_valid_db(CONFIG["dbfile"]):
            init_db_file()
        self._con = sqlite3.connect(CONFIG["dbfile"])
        self._con.execute("PRAGMA foreign_keys = ON")
        self._update_categories()

    def _update_categories(self):
        new_categories = set(CONFIG["categories"])
        query = "SELECT name FROM Categories"
        db_categories = set(x[0] for x in self._con.execute(query).fetchall())
        if db_categories != new_categories:
            to_be_deleted = db_categories - new_categories
            to_be_added = new_categories - db_categories
            for category in to_be_deleted:
                query = "DELETE FROM Categories WHERE name = ?"
                self._con.execute(query, [category])
            for category in to_be_added:
                query = "INSERT INTO Categories (name) VALUES (?)"
                self._con.execute(query, [category])
            self._con.commit()

    def _file_is_valid_db(self, path):
        if not (os.path.isfile(path) and os.access(path, os.R_OK)):
            return False
        con = sqlite3.connect(path)
        tables = ["Users", "Expenses", "Categories"]
        for table in tables:
            try:
                con.execute(f"SELECT * FROM {table}")
            except OperationalError:
                return False
        return True

    def get_user_by_username(self, username):
        """Hakee käyttäjän tietokannasta käyttäjänimen perusteella.

        Args:
            username: Käyttäjänimi

        Returns:
            Haluttua käyttäjää kuvaava User-objekti mikäli käyttäjä löytyi
            None jos haluttua käyttäjää ei löytynyt
        """
        query = "SELECT * FROM Users WHERE username = ?"
        results = self._con.execute(query, [username]).fetchone()
        if results:
            return User(results[1], results[2], results[0])
        return None

    def create_user(self, username, passwd):
        """Luo uuden käyttäjän tietokantaan.

        Args:
            username: Käyttäjänimi
            passwd: Salasana

        Returns:
            True jos käyttäjän luonti onnistui
            False jos käyttäjänimi on jo käytössä
        """
        query = "INSERT INTO Users (username, passwd) VALUES (?, ?)"
        try:
            self._con.execute(query, [username, passwd])
        except IntegrityError:
            self._con.commit()
            return False
        self._con.commit()
        return True

    def get_expenses(self, user_id):
        """Hakee halutun käyttäjän kaikki menot.

        Args:
            user_id: Käyttäjän id jonka menot halutaan hakea

        Returns:
            Lista, joka sisältää kaikki käyttäjän menot Expense-objekteina
        """
        query = """SELECT E.amount_int, E.amount_decimal, E.date, E.desc, C.name, E.id
                   FROM Expenses E, Categories C
                   WHERE E.user_id = ? AND C.id = E.category"""
        results = self._con.execute(query, [user_id]).fetchall()
        expenses = [Expense(amount_int=x[0],
                            amount_dec=x[1],
                            date=x[2],
                            desc=x[3],
                            category=x[4],
                            expense_id=x[5]) for x in results]
        return expenses

    def create_expense(self, user_id, amount_int, amount_dec, desc, category, time):
        """Luo uuden menon tietokantaan.

        Args:
            user_id: Käyttäjän id jolle meno halutaan luoda
            amount_int: Menon suuruuden kokonaisosa
            amount_dec: Menon suuruuden desimaaliosa
            desc: Sanallinen kuvaus menosta
            category: Menon kategoria (merkkijonona)
            time: Menon päivämäärä
        """
        query = """INSERT INTO Expenses (user_id, amount_int, amount_decimal, desc, category, date)
                   VALUES (?, ?, ?, ?, ?, ?)"""
        category_query = "SELECT id FROM Categories WHERE name = ?"
        category = int(self._con.execute(
            category_query, [category]).fetchone()[0])
        self._con.execute(query, [user_id, amount_int,
                                  amount_dec, desc, category, str(time)])
        self._con.commit()

    def delete_expense(self, expense_id):
        """Poistaa menon tietokannasta id:n perusteella.

        Args:
            expense_id: Menon id
        """
        query = "DELETE FROM Expenses WHERE id = ?"
        self._con.execute(query, [expense_id])
        self._con.commit()

    def get_month_expenses(self, user_id, year, month):
        """Hakee käyttäjän kaikki kuukauden menot.

        Args:
            user_id: Käyttäjän id
            year: Haluttu vuosi
            month: Haluttu kuukausi (kokonaislukuna)

        Returns:
            Lista, joka sisältää käyttäjän kuukauden menot Expense-objekteina
        """
        search_param = f"{year}-{month}%"
        query = """SELECT E.amount_int, E.amount_decimal, E.date, E.desc, C.name, E.id
                   FROM Expenses E, Categories C
                   WHERE C.id = E.category AND user_id = ? AND date like ?"""
        results = self._con.execute(query, [user_id, search_param])
        results = [Expense(e[0], e[1], e[2], e[3], e[4], e[5])
                   for e in results]
        return results
