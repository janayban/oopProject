import tkinter as tk

class AdminUI:
    def __init__(self, root):
        self.adminPage = tk.Toplevel(root)
        self.adminPage.configure(bg='white')
        self.adminPage.title("Admin Dashboard")
        self.adminPage.geometry("1000x700+280+70")

        # First method to be executed
        self.adminDashboardContent()


    def adminDashboardContent(self):
        adminLabel = tk.Label(self.adminPage, text="Admin Dashboard", bg='white', font=("Arial", 16))
        adminLabel.pack(pady=20)

