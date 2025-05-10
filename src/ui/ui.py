from tkinter import Tk
from ui.login_view import LoginView
from ui.main_view import MainView


class UI:
    """Sovelluksen käyttöliittymästä vastaava luokka.

    Attributes:
        current_view: Parhaillaan käytössä oleva näkymä
        window: Käyttöliittymän TkInter-ikkuna
    """

    def __init__(self):
        """Konstruktori, joka luo uuden käyttöliittymäinstanssin."""
        self.current_view = None
        self.window = Tk()

    def start(self):
        """Käynnistää käyttöliittymän."""
        self.current_view = LoginView(self.window, MainView)
        self.window.mainloop()
