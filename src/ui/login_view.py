from tkinter import ttk, constants

class LoginView:
    def __init__(self, root):
        self.root = root
        self.username = None
        self.passwd = None
        self.error_msg = None
        self._initialize()
    
    def _initialize(self):
        self._frame = ttk.Frame(self.root)

        login_label = ttk.Label(self.root, text="Log in")
        username_label = ttk.Label(self.root, text="Username:")
        passwd_label = ttk.Label(self.root, text="Password:")
        login_button = ttk.Button(self.root, text="Login")
        username_field = ttk.Entry(self.root)
        passwd_field = ttk.Entry(self.root, show="*")

        login_label.grid(row=0, column=0, columnspan=2, pady=6)
        username_label.grid(row=1, column=0, padx=6, pady=4)
        username_field.grid(row=1, column=1, padx=6, pady=4)
        passwd_label.grid(row=2, column=0, padx=6, pady=4)
        passwd_field.grid(row=2, column=1, padx=6, pady=4)
        login_button.grid(row=3, column=0, padx=6, pady=4)