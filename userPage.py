import tkinter as tk

class UserUI:
    def __init__(self, root, username):
        self.userPage = tk.Toplevel(root)
        self.userPage.configure(bg='white')
        self.userPage.title(f"{username} Dashboard")
        self.userPage.geometry("1000x700+280+70")

        # First method to be executed
        self.userUIContent()

    def userUIContent(self):
        self.userLabel = tk.Label(self.userPage, text="User Dashboard", bg='white', font=("Arial", 16))
        self.userLabel.pack(pady=20)
