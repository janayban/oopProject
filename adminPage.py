import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import style
import mysql.connector as mc


class AdminUI:
    def __init__(self, root):
        self.adminPage = tk.Toplevel(root)
        self.adminPage.configure(bg="#54742C")
        self.adminPage.title("Admin Dashboard")
        self.adminPage.geometry("990x500+280+70")
        self.adminPage.tk.call('tk', 'scaling', 2.0)

        # First method to be executed
        self.adminDashboardContent()

    def adminDashboardContent(self):
        pass