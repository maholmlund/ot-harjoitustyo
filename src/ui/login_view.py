from tkinter import ttk, constants, StringVar
from expensetracker import expensetracker
from ui.main_view import MainView


class LoginView:
    def __init__(self, root, handle_login):
        self.root = root
        self.error_msg = None
        self.handle_login = handle_login
        self._initialize()

    def _initialize(self):
        self._frame = ttk.Frame(self.root)

        self.username_field = ttk.Entry(self._frame)
        self.passwd_field = ttk.Entry(self._frame, show="*")
        self.error_label = ttk.Label(self._frame, textvariable=self.error_msg, foreground="red")

        login_label = ttk.Label(self._frame, text="Log in")
        username_label = ttk.Label(self._frame, text="Username:")
        passwd_label = ttk.Label(self._frame, text="Password:")
        login_button = ttk.Button(self._frame, text="Login", command=self._handle_login_submit)
        create_user_button = ttk.Button(self._frame, text="Create user", command=self._handle_user_creation)
        self.error_msg = StringVar(self._frame)

        self.username_field.grid(row=1, column=1, padx=6, pady=4)
        self.passwd_field.grid(row=2, column=1, padx=6, pady=4)
        self.error_label.grid(row=4, column=0, columnspan=2)
        login_label.grid(row=0, column=0, columnspan=2, pady=6)
        username_label.grid(row=1, column=0, padx=6, pady=4)
        passwd_label.grid(row=2, column=0, padx=6, pady=4)
        login_button.grid(row=3, column=0, padx=6, pady=4)
        create_user_button.grid(row=3, column=1, padx=6, pady=4)

        self._frame.pack()

    def _handle_login_submit(self):
        username = self.username_field.get()
        passwd = self.passwd_field.get()
        if not expensetracker.login(username, passwd):
            self.error_msg.set("Invalid username or password")
        else:
            self._frame.destroy()
            self.handle_login(self.root, LoginView)

    def _handle_user_creation(self):
        username = self.username.get()
        passwd = self.passwd.get()
        result = expensetracker.create_user(username, passwd)
        if type(result) is str:
            self.error_msg.set(result)
        else:
            self.error_msg.set("")
        self.error_label.grid()
