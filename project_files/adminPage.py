import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as mc
import loginSignup
import style
import cv2
from pyzbar.pyzbar import decode


class AdminUI:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.configure(bg="#54742C")
        self.root.title("Admin Dashboard")
        self.root.resizable(False, False)
        self.root.tk.call('tk', 'scaling', 2.0)

        self.bg = style.labelBgColor
        self.fg = style.labelTextColor
        self.font = style.userFontLabel

        # First method to be executed
        self.adminDashboardContent()


    # User Interface of Admin Window
    def adminDashboardContent(self):
        # Initializing the widgets and frames
        contentFrame = tk.Frame(self.root, bg="#54742C", padx=20)
        titleFrame = tk.Frame(self.root, bg="#DADBB1", height=100)
        titleLabel = tk.Label(titleFrame, text="ORAS - Registrar's Appointment Records", font=("Verdana", 20, "bold"),
                              bg="#DADBB1", fg="#000000")

        # Treeview for displaying records
        treeviewStyle = ttk.Style()
        treeviewStyle.configure("Treeview.Heading", foreground="black", font=("Arial", 10, "bold"))
        treeviewStyle.configure("Treeview", rowheight=30)

        columns = ("stud_num", "name", "course", "section", "appointment_type", "date", "time", "status")
        self.tree = ttk.Treeview(contentFrame, columns=columns, show="headings", height=15)
        self.tree.heading("stud_num", text="Student Number")
        self.tree.heading("name", text="Name")
        self.tree.heading("course", text="Course")
        self.tree.heading("section", text="Section")
        self.tree.heading("appointment_type", text="Appointment Type")
        self.tree.heading("date", text="Date")
        self.tree.heading("time", text="Time")
        self.tree.heading("status", text="Status")

        # Column widths
        self.tree.column("stud_num", width=170, anchor="center")
        self.tree.column("name", width=200, anchor="center")
        self.tree.column("course", width=150, anchor="center")
        self.tree.column("section", width=150, anchor="center")
        self.tree.column("appointment_type", width=260, anchor="center")
        self.tree.column("date", width=150, anchor="center")
        self.tree.column("time", width=150, anchor="center")
        self.tree.column("status", width=150, anchor="center")

        # Scrollbar for the Treeview
        treeScrollY = ttk.Scrollbar(contentFrame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=treeScrollY.set)

        # SearchFrame holds the search bar and different buttons
        searchFrame = tk.Frame(self.root, bg="#DADBB1", pady=10)

        searchLabel = tk.Label(searchFrame, text="Search by Student Number:", font=("Arial", 12), bg="#DADBB1")
        self.searchEntry = ttk.Entry(searchFrame, width=30)
        searchButton = ttk.Button(searchFrame, text="Search", command=self.searchStudent)
        deleteButton = ttk.Button(searchFrame, text="Delete Selected Record", command=self.deleteSelected)
        deleteAllButton = ttk.Button(searchFrame, text="Delete All Records", command=self.deleteAllRecords)
        showAllButton = ttk.Button(searchFrame, text="Show All Records", command=self.loadData)
        qrScanButton = ttk.Button(searchFrame, text="Scan QR Code", command=self.qrScanner)

        # Fetch data from the database
        self.loadData()

        # Different colors for alternating rows
        self.tree.tag_configure("evenrow", background="#F0F0F0")
        self.tree.tag_configure("oddrow", background="#FFFFFF")

        # Logout Button
        logoutFrame = tk.Frame(self.root, bg="#54742C", pady=10)
        logoutButton = tk.Button(logoutFrame, text="Log out", font=("Arial", 8), bg=style.accFrameColor,
                                 fg=style.accFgColor, activebackground=style.accFontColor, bd=0, command=self.logout)

        # Layout configuration for adminPage
        self.root.grid_rowconfigure(0, weight=0)  # Title Frame
        self.root.grid_rowconfigure(1, weight=0)  # Search Frame
        self.root.grid_rowconfigure(2, weight=1, minsize=200)  # Content Frame
        self.root.grid_rowconfigure(3, weight=0) # Logout Frame

        # Title Frame display
        titleFrame.grid(row=0, column=0, sticky="ew", ipady=15, pady=(0, 5))
        titleLabel.pack(expand=True, fill="both")

        # Search Bar Frame display
        searchFrame.grid(row=1, column=0, sticky="ew", padx=30, pady=10)
        searchLabel.grid(row=0, column=0, padx=5)
        self.searchEntry.grid(row=0, column=1, padx=5)
        searchButton.grid(row=0, column=2, padx=5)
        deleteButton.grid(row=0, column=3, padx=10)
        deleteAllButton.grid(row=0, column=4, padx=10)
        showAllButton.grid(row=0, column=5, padx=10)
        qrScanButton.grid(row=0, column=6, padx=10)

        # Display treeview and scrollbar to contentFrame
        contentFrame.grid(row=2, column=0, sticky="nsew", padx=10)
        self.tree.grid(row=0, column=0, sticky="nsew")
        treeScrollY.grid(row=0, column=1, sticky="ns")

        # Layout configuration of contentFrame
        contentFrame.grid_columnconfigure(0, weight=1)
        contentFrame.grid_rowconfigure(0, weight=1)

        logoutFrame.grid(row=3, column=0, sticky="e", padx=30)
        logoutButton.pack(expand=True, fill="both")

        # Bind click event to the Treeview
        self.tree.bind("<Button-1>", lambda event: self.OnTreeViewClick(event, self.tree, contentFrame))


    # Method for editing the "status" column
    def OnTreeViewClick(self, event, tree, contentFrame):
        # Identify the selected item and column
        item = tree.identify_row(event.y)
        column = tree.identify_column(event.x)

        # Check if the clicked column is the "status" column
        if column == "#8" and item:
            currentValues = tree.item(item, "values")
            currentStatus = currentValues[7]

            statusOptions = ["Pending", "Finished", "Cancelled", "In Progress"]

            combobox = ttk.Combobox(contentFrame, values=statusOptions, state="readonly")
            combobox.set(currentStatus)
            combobox.focus()

            bbox = tree.bbox(item, column)
            if not bbox:
                return

            combobox.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])

            # Method used to save the new status
            def saveStatus():
                nonlocal statusSaved
                if statusSaved:
                    return

                statusSaved = True

                newStatus = combobox.get()

                if newStatus and newStatus != currentStatus:
                    newValues = list(currentValues)
                    newValues[7] = newStatus
                    tree.item(item, values=newValues)

                    try:
                        connection = mc.connect(host="localhost", user="root", password="",database="oras_trial")
                        cursor = connection.cursor()
                        cursor.execute(
                            "UPDATE user_input_forms SET status = %s WHERE stud_num = %s",
                            (newStatus, currentValues[0])
                        )
                        connection.commit()
                        cursor.close()
                        connection.close()
                        messagebox.showinfo("Success", "Status updated successfully.")
                    except mc.Error as e:
                        messagebox.showerror("Database Error", f"Failed to update status: {e}")

                combobox.destroy()

            statusSaved = False

            # Bind events to the Combobox
            combobox.bind("<<ComboboxSelected>>", lambda _: saveStatus())  # Detect option selection
            combobox.bind("<FocusOut>", lambda _: saveStatus())  # Trigger on losing focus


    # Method used to fetch all the data
    def loadData(self):
        try:
            connection = mc.connect(host="localhost", user="root", password="",database="oras_trial")
            cursor = connection.cursor()
            cursor.execute(
                "SELECT stud_num, name, course, section, appointment_type, date, time, status FROM user_input_forms"
            )
            rows = cursor.fetchall()
            self.tree.delete(*self.tree.get_children())  # Clear existing rows
            for index, row in enumerate(rows):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=row, tags=(tag,))

            cursor.close()
            connection.close()
        except mc.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")


    # Method used to search student by student number
    def searchStudent(self):
        # Get the student number value from Search Entry
        studentNumber = self.searchEntry.get()

        if not studentNumber:
            messagebox.showwarning("Input Error", "Please enter a student number to search.")
            return

        # Search for a record by student number
        try:
            connection = mc.connect(host="localhost", user="root", password="",database="oras_trial")
            cursor = connection.cursor()
            query = "SELECT stud_num, name, course, section, appointment_type, date, time, status FROM user_input_forms WHERE stud_num = %s"
            cursor.execute(query, (studentNumber,))
            rows = cursor.fetchall()

            self.tree.delete(*self.tree.get_children())

            if rows:
                # Display the result if found after iterating in the database
                for index, row in enumerate(rows):
                    tag = "evenrow" if index % 2 == 0 else "oddrow"
                    self.tree.insert("", "end", values=row, tags=(tag,))

            else:
                messagebox.showinfo("No Results", f"No record found for student number {studentNumber}.")
                self.loadData()  # Reload all records

            cursor.close()
            connection.close()

        except mc.Error as e:
            messagebox.showerror("Database Error", f"An error occurred during search: {e}")


    # Method used to delete a selected record
    def deleteSelected(self):
        selectedItem = self.tree.selection()
        if selectedItem:
            record = self.tree.item(selectedItem)["values"]
            studentNumber = record[0]
            if messagebox.askyesno("Confirm Delete",
                                   "Are you sure you want to delete this record? This action cannot be undone."):

                try:
                    connection = mc.connect(host="localhost", user="root", password="",database="oras_trial")
                    cursor = connection.cursor()
                    cursor.execute("DELETE FROM user_input_forms WHERE stud_num = %s", (studentNumber,))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    self.tree.delete(selectedItem)  # Remove the row from the Treeview
                    messagebox.showinfo("Success", "Record deleted successfully.")
                except mc.Error as e:
                    messagebox.showerror("Database Error", f"Failed to delete record: {e}")
        else:
            messagebox.showwarning("Selection Error", "Please select a record to delete.")


    # Method used to delete all records at once
    def deleteAllRecords(self):
        # Delete all records from the database
        if messagebox.askyesno("Confirm Delete",
                               "Are you sure you want to delete all records? This action cannot be undone."):

            try:
                connection = mc.connect(host="localhost", user="root", password="",database="oras_trial")
                cursor = connection.cursor()

                # Check if there are any records in the table
                cursor.execute("SELECT COUNT(*) FROM user_input_forms")
                recordCount = cursor.fetchone()[0]

                if recordCount == 0:
                    # If there are no records to delete, show a message and exit
                    messagebox.showinfo("No Records", "There are no records to delete.")
                else:
                    # Delete all records from the table
                    cursor.execute("DELETE FROM user_input_forms")
                    connection.commit()

                    # Clear all items from the Treeview widget
                    self.tree.delete(*self.tree.get_children())

                    # Show success message
                    messagebox.showinfo("Success", "All records deleted successfully.")

                # Close cursor and connection
                cursor.close()
                connection.close()

            except mc.Error as e:
                messagebox.showerror("Database Error", f"Failed to delete all records: {e}")
            except Exception as ex:
                messagebox.showerror("Error", f"An unexpected error occurred: {ex}")


    # Method used for QR Scanner
    def qrScanner(self):
        cam = cv2.VideoCapture(0)
        cam.set(5, 640)
        cam.set(6, 480)

        camera = True

        while camera:
            success, frame = cam.read()
            if not success:
                break

            for i in decode(frame):
                scanned_value = i.data.decode("utf-8")

                # Set the scanned QR code value in the search entry
                self.searchEntry.delete(0, tk.END)  # Clear the existing text
                self.searchEntry.insert(0, scanned_value)  # Insert the scanned value

                self.searchStudent()

                messagebox.showinfo("QR Code Scanned", "Scanned successfully!")
                break

            cv2.imshow("QR_Code_Scanner", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

            if cv2.getWindowProperty("QR_Code_Scanner", cv2.WND_PROP_VISIBLE) < 1:
                break

        cam.release()
        cv2.destroyAllWindows()


    # Method used for Logout
    def logout(self):
        confirm = messagebox.askyesno("Logout Confirmation", "Are you sure you want to log out?")

        if confirm:
            self.root.withdraw()
            loginPage = loginSignup.LoginSignUp(self.root)
            self.root.deiconify()