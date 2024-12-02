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
        self.adminPage.geometry("1500x600+45+70")
        self.adminPage.resizable(False, False)
        self.adminPage.tk.call('tk', 'scaling', 2.0)

        self.bg = style.labelBgColor
        self.fg = style.labelTextColor
        self.font = style.userFontLabel

        # First method to be executed
        self.adminDashboardContent()

    def adminDashboardContent(self):
        # Main frame for the content with a darker background color
        contentFrame = tk.Frame(self.adminPage, bg="#54742C", padx=20, pady=20)

        # Create a frame for the title with a lighter background color
        titleFrame = tk.Frame(self.adminPage, bg="#DADBB1", height=100)  # Fixed height for title frame

        # Add title label inside the title frame
        titleLabel = tk.Label(
            titleFrame,
            text="ORAS - Registrar's Appointment Records",
            font=("Verdana", 20, "bold"),
            bg="#DADBB1",  # Match the frame background color
            fg="#000000"  # Black text color
        )

        # Define style for the Treeview headings (highlighting)
        style = ttk.Style()
        style.configure("Treeview.Heading",
                        foreground="black",  # White text color
                        font=("Arial", 10, "bold"))  # Bold Arial font

        # Treeview for displaying records
        columns = ("stud_num", "name", "course", "section", "appointment_type", "date", "time", "status")
        tree = ttk.Treeview(contentFrame, columns=columns, show="headings", height=15)
        tree.heading("stud_num", text="Student Number")
        tree.heading("name", text="Name")
        tree.heading("course", text="Course")
        tree.heading("section", text="Section")
        tree.heading("appointment_type", text="Appointment Type")
        tree.heading("date", text="Date")
        tree.heading("time", text="Time")
        tree.heading("status", text="Status")

        # Setting column widths
        tree.column("stud_num", width=170, anchor="center")
        tree.column("name", width=200, anchor="center")  # Increased width for Name column
        tree.column("course", width=150, anchor="center")
        tree.column("section", width=150, anchor="center")
        tree.column("appointment_type", width=260, anchor="center")  # Increased width for Appointment Type column
        tree.column("date", width=150, anchor="center")
        tree.column("time", width=150, anchor="center")
        tree.column("status", width=150, anchor="center")

        # Create a custom style to add row padding
        style.configure("Treeview", rowheight=30)  # Adjust this value to control row height

        # Scrollbars for the Treeview
        tree_scroll_y = ttk.Scrollbar(contentFrame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=tree_scroll_y.set)

        # Fetch data from database
        try:
            connection = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="oras_trial"
            )
            cursor = connection.cursor()
            cursor.execute(
                "SELECT stud_num, name, course, section, appointment_type, date, time, status FROM user_input_forms")
            rows = cursor.fetchall()

            # Insert data into the Treeview
            for index, row in enumerate(rows):
                # Apply alternating row colors to simulate spacing
                if index % 2 == 0:
                    tree.insert("", "end", values=row, tags=("evenrow",))
                else:
                    tree.insert("", "end", values=row, tags=("oddrow",))

            # Close database connection
            cursor.close()
            connection.close()
        except mc.Error as e:
            messagebox.showerror("Database Error", f"An error occurred while fetching data: {e}")

        # Add custom styles for row spacing effect
        tree.tag_configure("evenrow", background="#F0F0F0")  # Light gray background for even rows
        tree.tag_configure("oddrow", background="#FFFFFF")  # White background for odd rows

        # Layout configuration
        self.adminPage.grid_rowconfigure(0, weight=0)  # Title row
        self.adminPage.grid_rowconfigure(1, weight=1)  # Content row
        self.adminPage.grid_columnconfigure(0, weight=1)

        # Title Frame
        titleFrame.grid(row=0, column=0, sticky="ew", ipady=15)
        titleLabel.pack(expand=True, fill="both")

        # Add Treeview and scrollbars to contentFrame
        contentFrame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        tree.grid(row=0, column=0, sticky="nsew")
        tree_scroll_y.grid(row=0, column=1, sticky="ns")


        # Adjust layout of contentFrame
        contentFrame.grid_columnconfigure(0, weight=1)
        contentFrame.grid_rowconfigure(0, weight=1)
