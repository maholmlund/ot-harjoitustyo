from tkinter import Tk
from ui.login_view import LoginView
from ui.main_view import MainView
from expensetracker import Expensetracker

expensetracker = Expensetracker()

class UI:
    def __init__(self):
        self.current_view = None
        self.window = Tk()
    
    def start(self):
        self.current_view = LoginView(self.window, MainView)
        self.window.mainloop()
