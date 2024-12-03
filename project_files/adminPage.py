import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as mc
import style
import cv2
from pyzbar.pyzbar import decode


class AdminUI:
    def __init__(self, root):
        self.adminPage = tk.Toplevel(root)
        self.adminPage.configure(bg="#54742C")
        self.adminPage.title("Admin Dashboard")
        self.adminPage.resizable(False, False)
        self.adminPage.tk.call('tk', 'scaling', 2.0)

        self.bg = style.labelBgColor
        self.fg = style.labelTextColor
        self.font = style.userFontLabel

        # First method to be executed
        self.adminDashboardContent()

    def adminDashboardContent(self):
        # Frame where all the widgets below the title is placed
        contentFrame = tk.Frame(self.adminPage, bg="#54742C", padx=20, pady=10)

        # Frame where the title is placed
        titleFrame = tk.Frame(self.adminPage, bg="#DADBB1", height=100)

        # Label placed within the title frame
        titleLabel = tk.Label(
            titleFrame,
            text="ORAS - Registrar's Appointment Records",
            font=("Verdana", 20, "bold"),
            bg="#DADBB1",
            fg="#000000"
        )

        # Style for treeview Headings
        treeviewStyle = ttk.Style()
        treeviewStyle.configure(
            "Treeview.Heading",
            foreground="black",
            font=("Arial", 10, "bold")
        )

        # Treeview for displaying records
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

        # Row height spacing
        treeviewStyle.configure("Treeview", rowheight=30)

        # Scrollbar for the Treeview
        treeScrollY = ttk.Scrollbar(contentFrame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=treeScrollY.set)

        # SearchFrame holds the search bar and different buttons
        searchFrame = tk.Frame(self.adminPage, bg="#DADBB1", pady=10)

        searchLabel = tk.Label(searchFrame, text="Search by Student Number:", font=("Arial", 12), bg="#DADBB1")
        self.searchEntry = ttk.Entry(searchFrame, width=30)
        searchButton = ttk.Button(searchFrame, text="Search",
                                  command=self.searchStudent)
        deleteButton = ttk.Button(searchFrame, text="Delete Selected Record",
                                  command=self.deleteSelected)
        deleteAllButton = ttk.Button(searchFrame, text="Delete All Records", command=self.deleteAllRecords)
        showAllButton = ttk.Button(searchFrame, text="Show All Records", command=self.loadData)
        qrScanButton = ttk.Button(searchFrame, text="Scan QR Code", command=self.qrScanner)

        # Fetch data from the database
        self.loadData()

        # Different colors for alternating rows
        self.tree.tag_configure("evenrow", background="#F0F0F0")
        self.tree.tag_configure("oddrow", background="#FFFFFF")

        # Layout configuration for adminPage
        self.adminPage.grid_rowconfigure(0, weight=0)  # Title frame doesn't expand
        self.adminPage.grid_rowconfigure(1, weight=0)  # Search frame doesn't expand
        self.adminPage.grid_rowconfigure(2, weight=1, minsize=200)  # Content frame takes up remaining space

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
        contentFrame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.tree.grid(row=0, column=0, sticky="nsew")
        treeScrollY.grid(row=0, column=1, sticky="ns")

        # Layout configuration of contentFrame
        contentFrame.grid_columnconfigure(0, weight=1)
        contentFrame.grid_rowconfigure(0, weight=1)

        # Bind double-click event to the Treeview
        self.tree.bind("<Double-1>", lambda event: self.OnTreeViewDoubleClick(event, self.tree, contentFrame))


    # Function for Editing the "status" column
    def OnTreeViewDoubleClick(self, event, tree, contentFrame):
        # Identify the selected item and column
        item = tree.identify_row(event.y)
        column = tree.identify_column(event.x)

        # Check if the clicked column is the "status" column
        if column == "#8":
            # Get current values of the row
            currentValues = tree.item(item, "values")
            currentStatus = currentValues[7]

            # Create an Entry widget for editing
            entry = ttk.Entry(contentFrame)
            entry.insert(0, currentStatus)
            entry.focus()

            # Position the Entry widget over the cell
            bbox = tree.bbox(item, column)
            entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])

            def saveStatus():
                entry.unbind("<Return>")
                entry.unbind("<FocusOut>")

                # Get new status value
                newStatus = entry.get()
                if newStatus:
                    # Update the Treeview
                    newValues = list(currentValues)
                    newValues[7] = newStatus
                    tree.item(item, values=newValues)

                    # Update the database
                    try:
                        connection = mc.connect(
                            host="localhost",
                            user="root",
                            password="",
                            database="oras_trial"
                        )
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
                else:
                    messagebox.showwarning("Input Error", "Status cannot be empty.")

                # Destroy the Entry widget
                entry.destroy()

            # Bind events to the Entry widget
            entry.bind("<Return>", lambda _: saveStatus())
            entry.bind("<FocusOut>", lambda _: saveStatus())


    # Method used to fetch all the data
    def loadData(self):
        try:
            connection = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="oras_trial"
            )
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
            connection = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="oras_trial"
            )
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

    # Function to delete a selected record
    def deleteSelected(self):
        selectedItem = self.tree.selection()
        if selectedItem:
            record = self.tree.item(selectedItem)["values"]
            studentNumber = record[0]
            if messagebox.askyesno("Confirm Delete",
                                   "Are you sure you want to delete this record? This action cannot be undone."):

                try:
                    connection = mc.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="oras_trial"
                    )
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


    # Function to delete all records at once
    def deleteAllRecords(self):
        # Delete all records from the database
        if messagebox.askyesno("Confirm Delete",
                               "Are you sure you want to delete all records? This action cannot be undone."):

            try:
                # Establish connection to the database
                connection = mc.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="oras_trial"
                )
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

    # Function for QR Scanner
    def qrScanner(self):
        cam = cv2.VideoCapture(0)
        cam.set(5, 640)
        cam.set(6, 480)

        camera = True

        while camera:
            success, frame = cam.read()
            if not success:
                break

            # Decode the QR code(s) in the frame
            for i in decode(frame):
                scanned_value = i.data.decode("utf-8")

                # Set the scanned QR code value in the search entry
                self.searchEntry.delete(0, tk.END)  # Clear the existing text
                self.searchEntry.insert(0, scanned_value)  # Insert the scanned value

                # Automatically trigger the search function
                self.searchStudent()

                messagebox.showinfo("QR Code Scanned", "Scanned successfully!")

                # Break after one scan to prevent continuous scanning
                break

            # Display the camera frame with QR code detection
            cv2.imshow("QR_Code_Scanner", frame)

            # Check for user closing the window (pressing "X")
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # If the user presses 'q' (or any key you choose)
                break

            # Check if the window is closed by "X" button
            if cv2.getWindowProperty("QR_Code_Scanner", cv2.WND_PROP_VISIBLE) < 1:
                break

        # Release resources and close window
        cam.release()
        cv2.destroyAllWindows()

