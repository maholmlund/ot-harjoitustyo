from tkinter import ttk, constants, StringVar
from expensetracker import expensetracker
from ui.main_view import MainView


class LoginView:
    def __init__(self, root, handle_login):
        self._root = root
        self._frame = ttk.Frame(self._root)
        self._error_msg = StringVar(self._frame)
        self._info_msg = StringVar(self._frame)
        self._handle_login = handle_login
        self._username_field = None
        self._passwd_field = None

        self._initialize()

    def _initialize(self):
        self._username_field = ttk.Entry(self._frame)
        self._passwd_field = ttk.Entry(self._frame, show="*")
        error_label = ttk.Label(self._frame, textvariable=self._error_msg, foreground="red")
        info_label = ttk.Label(self._frame, textvariable=self._info_msg)

        login_label = ttk.Label(self._frame, text="Log in")
        username_label = ttk.Label(self._frame, text="Username:")
        passwd_label = ttk.Label(self._frame, text="Password:")
        login_button = ttk.Button(self._frame, text="Login", command=self._handle_login_submit)
        create_user_button = ttk.Button(self._frame, text="Create user", command=self._handle_user_creation)

        self._username_field.grid(row=1, column=1, padx=6, pady=4)
        self._passwd_field.grid(row=2, column=1, padx=6, pady=4)
        error_label.grid(row=4, column=0, columnspan=2)
        info_label.grid(row=5, column=0, columnspan=2)
        login_label.grid(row=0, column=0, columnspan=2, pady=6)
        username_label.grid(row=1, column=0, padx=6, pady=4)
        passwd_label.grid(row=2, column=0, padx=6, pady=4)
        login_button.grid(row=3, column=0, padx=6, pady=4)
        create_user_button.grid(row=3, column=1, padx=6, pady=4)

        self._frame.pack()

    def _handle_login_submit(self):
        username = self._username_field.get()
        passwd = self._passwd_field.get()
        self._info_msg.set("")
        if not expensetracker.login(username, passwd):
            self._error_msg.set("Invalid username or password")
        else:
            self._frame.destroy()
            self._handle_login(self._root, LoginView)

    def _handle_user_creation(self):
        username = self._username_field.get()
        passwd = self._passwd_field.get()
        self._info_msg.set("")
        result = expensetracker.create_user(username, passwd)
        if type(result) is str:
            self._error_msg.set(result)
        else:
            self._error_msg.set("")
            self._info_msg.set("User created")
        self._initialize()
