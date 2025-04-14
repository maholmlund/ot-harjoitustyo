from tkinter import ttk, Tk
from ui.login_view import LoginView
from ui.main_view import MainView


class UI:
    def __init__(self):
        self.current_view = None
        self.window = Tk()
        style = ttk.Style(self.window)
        style.theme_use('breeze')

    def start(self):
        self.current_view = LoginView(self.window, MainView)
        self.window.mainloop()
