import tkinter as tk
from tkinter import messagebox
import mysql.connector as mc
import hashlib as hash
import adminPage
import userPage

connect = mc.connect(host='localhost', database='oras_trial', user='root', password='')
cursor = connect.cursor()

class LoginSignUp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login/Signup")
        self.root.geometry("400x400+600+200")
        self.root.resizable(False, False)
        self.root.configure(bg="#3b3b3b")

        # Initialize login UI by default
        self.loginUI()

    def clearWindow(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def hashPassword(self, password):
        # Hash the password using SHA-256 // [:16] stores only the first 16 characters
        return hash.sha256(password.encode()).hexdigest()[:16]

    def loginUI(self):
        self.clearWindow()

        #Initializing the widgets
        loginLabel = tk.Label(self.root, text="Login", font=("Arial", 24, "bold"), bg="#3b3b3b", fg="#ecf0f1")

        frame = tk.Frame(self.root, bg="#4f4f4f", padx=20, pady=20)

        usernameLabel = tk.Label(frame, text="Username", font=("Arial", 12), bg="#4f4f4f", fg="#ecf0f1")
        self.usernameLoginEntry = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", fg="#3b3b3b", borderwidth=2, relief="groove")

        passwordLabel = tk.Label(frame, text="Password", font=("Arial", 12), bg="#4f4f4f", fg="#ecf0f1")
        self.passwordLoginEntry = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", fg="#3b3b3b", borderwidth=2, relief="groove", show="*")

        loginButton = tk.Button(self.root, text="Login", font=("Arial", 12), bg="#5a5a5a", fg="white", activebackground="#4b4b4b", command=self.login)

        noAccountButton = tk.Button(self.root, text="Don't have an account? Sign up", font=("Arial", 10), bg="#3b3b3b", fg="#a0c4ff", activebackground="#3b3b3b", bd=0, command=self.signupUI)

        # Displaying the widgets
        loginLabel.pack(pady=20)
        frame.pack(pady=10, padx=10, fill="both", expand=True)
        usernameLabel.pack(anchor="w", pady=7)
        self.usernameLoginEntry.pack(fill="x", pady=5)
        passwordLabel.pack(anchor="w", pady=7)
        self.passwordLoginEntry.pack(fill="x", pady=5)
        loginButton.pack(pady=15, padx=20, ipadx=10)
        noAccountButton.pack()

    def signupUI(self):
        self.clearWindow()

        #Initializing the widgets
        signupLabel = tk.Label(self.root, text="Sign Up", font=("Arial", 24, "bold"), bg="#3b3b3b", fg="#ecf0f1")

        frame = tk.Frame(self.root, bg="#4f4f4f", padx=20, pady=20)

        usernameLabel = tk.Label(frame, text="Username", font=("Arial", 12), bg="#4f4f4f", fg="#ecf0f1")
        self.usernameSignupEntry = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", fg="#3b3b3b", borderwidth=2, relief="groove")

        passwordLabel = tk.Label(frame, text="Password", font=("Arial", 12), bg="#4f4f4f", fg="#ecf0f1")
        self.passwordSignupEntry = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", fg="#3b3b3b", borderwidth=2, relief="groove", show="*")

        confirmPasswordLabel = tk.Label(frame, text="Confirm Password", font=("Arial", 12), bg="#4f4f4f", fg="#ecf0f1")
        self.confirmPasswordEntry = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", fg="#3b3b3b", borderwidth=2, relief="groove", show="*")

        signupButton = tk.Button(self.root, text="Sign Up", font=("Arial", 12), bg="#5a5a5a", fg="white", activebackground="#4b4b4b", command=self.signup)

        haveAccountButton = tk.Button(self.root, text="Already have an account? Log in", font=("Arial", 10), bg="#3b3b3b", fg="#a0c4ff", activebackground="#3b3b3b", bd=0, command=self.loginUI)

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
                    self.clearWindow()
                    self.root.withdraw()

                    # Goes to Admin's UI
                    adminPage.AdminUI(self.root)


                else:
                    messagebox.showinfo("Login Success", f"Welcome, {username}!")
                    self.clearWindow()
                    self.root.withdraw()

                    # Goes to User's UI
                    userPage.UserUI(self.root, username)

                    # userPage = tk.Toplevel(self.root)
                    # userPage.configure(bg='white')
                    # userPage.title(f"{username} Dashboard")
                    # userPage.geometry("1000x700+280+70")
                    # userLabel = tk.Label(userPage, text="User Dashboard", bg='white', font=("Arial", 16))
                    # userLabel.pack(pady=20)
            else:
                messagebox.showerror("Login Failed", "Invalid credentials, please try again.")
        else:
            messagebox.showerror("Error", "Please enter both username and password.")

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
                        connect.commit()

                        messagebox.showinfo("Signup Success", "Account created successfully!")
                        self.loginUI()
                else:
                    messagebox.showerror("Error", "Password fields are required.")
        else:
            messagebox.showerror("Error", "Username is required.")