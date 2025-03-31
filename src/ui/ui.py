from tkinter import Tk
from ui.login_view import LoginView
from expensetracker import Expensetracker

expensetracker = Expensetracker()

class UI:
    def __init__(self):
        self.current_view = None
        self.window = Tk()
    
    def start(self):
        self.current_view = LoginView(self.window)
        self.window.mainloop()
