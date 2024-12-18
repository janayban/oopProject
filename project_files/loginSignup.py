import tkinter as tk
from tkinter import messagebox
import mysql.connector as mc
import hashlib as hash
import adminPage
import userPage
import style

connection = mc.connect(host='localhost', database='oras_trial', user='root', password='')
cursor = connection.cursor()


class LoginSignUp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login/Signup")
        self.root.geometry("400x400+600+200")
        self.root.resizable(False, False)
        self.root.configure(bg=style.accBgColor)

        # Initialize login UI by default
        self.loginUI()


    # User Interface of Login
    def loginUI(self):
        self.clearWindow()

        #Initializing the widgets
        loginLabel = tk.Label(self.root, text="Login", font=("Arial", 24, "bold"), bg=style.accBgColor,
                              fg=style.accFontColor)

        frame = tk.Frame(self.root, bg=style.accFrameColor, padx=20, pady=20)

        usernameLabel = tk.Label(frame, text="Username", font=("Arial", 12), bg=style.accFrameColor,
                                 fg=style.accFgColor)
        self.usernameLoginEntry = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", fg="#3b3b3b", borderwidth=2,
                                           relief="groove")

        passwordLabel = tk.Label(frame, text="Password", font=("Arial", 12), bg=style.accFrameColor,
                                 fg=style.accFgColor)
        self.passwordLoginEntry = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", fg="#3b3b3b", borderwidth=2,
                                           relief="groove", show="*")

        loginButton = tk.Button(self.root, text="Login", font=("Arial", 12), bg="#2e4718", fg="white",
                                activebackground=style.accFrameColor, command=self.login)

        noAccountButton = tk.Button(self.root, text="Don't have an account? Sign up", font=("Arial", 10),
                                    bg=style.accBgColor, fg="#94daff", activebackground=style.accBgColor,
                                    bd=0, command=self.signupUI)

        # Displaying the widgets
        loginLabel.pack(pady=20)
        frame.pack(pady=10, padx=10, fill="both", expand=True)
        usernameLabel.pack(anchor="w", pady=7)
        self.usernameLoginEntry.pack(fill="x", pady=5)
        passwordLabel.pack(anchor="w", pady=7)
        self.passwordLoginEntry.pack(fill="x", pady=5)
        loginButton.pack(pady=15, padx=20, ipadx=10)
        noAccountButton.pack()


    # User Interface of Sign up
    def signupUI(self):
        self.clearWindow()

        #Initializing the widgets
        signupLabel = tk.Label(self.root, text="Sign Up", font=("Arial", 24, "bold"), bg=style.accBgColor,
                               fg=style.accFontColor)

        frame = tk.Frame(self.root, bg=style.accFrameColor, padx=20, pady=20)

        usernameLabel = tk.Label(frame, text="Username", font=("Arial", 12), bg=style.accFrameColor,
                                 fg=style.accFgColor)
        self.usernameSignupEntry = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", fg="#3b3b3b", borderwidth=2,
                                            relief="groove")

        passwordLabel = tk.Label(frame, text="Password", font=("Arial", 12), bg=style.accFrameColor,
                                 fg=style.accFgColor)
        self.passwordSignupEntry = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", fg="#3b3b3b", borderwidth=2,
                                            relief="groove", show="*")

        confirmPasswordLabel = tk.Label(frame, text="Confirm Password", font=("Arial", 12), bg=style.accFrameColor,
                                        fg=style.accFgColor)
        self.confirmPasswordEntry = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", fg="#3b3b3b", borderwidth=2,
                                             relief="groove", show="*")

        signupButton = tk.Button(self.root, text="Sign Up", font=("Arial", 12), bg="#2e4718",
                                 fg="white", activebackground=style.accFrameColor, command=self.signup)

        haveAccountButton = tk.Button(self.root, text="Already have an account? Log in", font=("Arial", 10),
                                      bg=style.accBgColor, fg="#94daff", activebackground=style.accBgColor,
                                      bd=0, command=self.loginUI)

        # Display the widgets
        signupLabel.pack(pady=20)
        frame.pack(pady=10, padx=10, fill="both", expand=True)
        usernameLabel.pack(anchor="w")
        self.usernameSignupEntry.pack(fill="x", pady=5)
        passwordLabel.pack(anchor="w")
        self.passwordSignupEntry.pack(fill="x", pady=5)
        confirmPasswordLabel.pack(anchor="w")
        self.confirmPasswordEntry.pack(fill="x", pady=5)
        signupButton.pack(pady=15, padx=20, ipadx=10)
        haveAccountButton.pack()


    # Logic and conditions for Login
    def login(self):
        username = self.usernameLoginEntry.get()
        password = self.passwordLoginEntry.get()

        if username and password:
            # Hash the entered password for comparison
            hashedPassword = self.hashPassword(password)

            loginQuery = f"SELECT username, password FROM accounts WHERE username = '{username}' AND password ='{hashedPassword}'"
            cursor.execute(loginQuery)
            result = cursor.fetchone()

            if result:
                if username == "registrar":
                    messagebox.showinfo("Login Success", "Welcome, Admin!")
                    self.root.withdraw()

                    # Goes to Admin's UI
                    adminPage.AdminUI(self.root)

                else:
                    messagebox.showinfo("Login Success", f"Welcome, {username}!")
                    self.root.withdraw()

                    # Goes to User's UI
                    userPage.UserUI(self.root, username)

            else:
                messagebox.showerror("Login Failed", "Invalid credentials, please try again.")
        else:
            messagebox.showerror("Error", "Please enter both username and password.")


    # Logic and conditions for Sign up
    def signup(self):
        username = self.usernameSignupEntry.get()
        password = self.passwordSignupEntry.get()
        confirm_password = self.confirmPasswordEntry.get()

        if username:
            if len(username) < 5:
                messagebox.showerror("Error", "Username must be at least 5 characters long.")
            else:
                checkQuery = f"SELECT * FROM accounts WHERE username = '{username}'"
                cursor.execute(checkQuery)
                result = cursor.fetchone()

                if result:
                    messagebox.showerror("Error", "Username already exists. Please choose a different username.")
                elif password and confirm_password:
                    if len(password) < 8:
                        messagebox.showerror("Error", "Password must be at least 8 characters long.")
                    elif password != confirm_password:
                        messagebox.showerror("Error", "Passwords do not match.")
                    else:
                        hashedPassword = self.hashPassword(password)

                        query = f"INSERT INTO accounts(username, password) VALUES ('{username}', '{hashedPassword}')"
                        cursor.execute(query)
                        connection.commit()

                        messagebox.showinfo("Signup Success", "Account created successfully!")
                        self.loginUI()
                else:
                    messagebox.showerror("Error", "Password fields are required.")
        else:
            messagebox.showerror("Error", "Username is required.")


    # Method for clearing widgets
    def clearWindow(self):
        for widget in self.root.winfo_children():
            widget.destroy()


    # Encrypting the password // [:16] stores only the first 16 characters
    def hashPassword(self, password):
        return hash.sha256(password.encode()).hexdigest()[:16]
