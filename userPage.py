import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import style
import mysql.connector as mc


class UserUI:
    def __init__(self, root, username):
        self.userPage = tk.Toplevel(root)
        self.userPage.configure(bg="#54742C")
        self.userPage.title(f"{username} Appointment Form")
        self.userPage.geometry("990x500+280+70")
        self.userPage.resizable(False, False)
        self.userPage.tk.call('tk', 'scaling', 2.0)  # Doubles the default size
        self.bg = style.labelBgColor
        self.fg = style.labelTextColor
        self.font = style.userFontLabel

        # First method to be executed
        self.userUIContent()

    def userUIContent(self):
        # Main frame with a darker background color
        contentFrame = tk.Frame(self.userPage, bg="#54742C", padx=20, pady=20)  # Darker background (swapped)

        # Create a frame for the title with a lighter background color
        titleFrame = tk.Frame(contentFrame, bg="#DADBB1", height=100)  # Lighter background (swapped)

        # Add title label inside the colored frame
        titleLabel = tk.Label(
            titleFrame,
            text="ORAS: Office of the Registrar Appointment System",
            font=("Verdana", 16, "bold"),
            bg="#DADBB1",  # Match the new frame background color
            fg="#000000"   # Black text color
        )

        #Initializing the widgets
        studNumLabel = tk.Label(contentFrame, text="Student Number:", font=self.font, bg=self.bg, fg=self.fg)
        self.studNumEntry = tk.Entry(contentFrame, width=30)

        nameLabel = tk.Label(contentFrame, text="Name:", font=self.font, bg=self.bg, fg=self.fg)
        self.nameEntry = tk.Entry(contentFrame, width=30)

        appTypeLabel = tk.Label(contentFrame, text="Appointment Type:", font=self.font, bg=self.bg, fg=self.fg)
        self.appTypeCheckBox = ttk.Combobox(contentFrame, values=["Certificate of Registration (COR)",
                                                                  "Transcript of Records (TOR)",
                                                                  "Others (Please Specify)"], width=28,
                                                                   state="readonly")

        self.appTypeCheckBox.bind("<<ComboboxSelected>>", self.toggleOthersEntry)  # Bind selection event

        dateLabel = tk.Label(contentFrame, text="Select Date:", font=self.font, bg=self.bg, fg=self.fg)
        self.dateEntry = tk.Entry(contentFrame, width=30)
        self.dateEntry.insert(0, " yyyy-mm-dd")

        # Bind the date entry click to trigger pickDate
        self.dateEntry.bind("<1>", self.pickDate)

        courseLabel = tk.Label(contentFrame, text="Course:", font=self.font, bg=self.bg, fg=self.fg)
        self.courseEntry = tk.Entry(contentFrame, width=30)

        sectionLabel = tk.Label(contentFrame, text="Section:", font=self.font, bg=self.bg, fg=self.fg)
        self.sectionEntry = tk.Entry(contentFrame, width=30)

        self.othersLabel = tk.Label(contentFrame, text="Others:", font=self.font, bg=self.bg, fg=self.fg,
                               disabledforeground="#3b3b3b" , state="disabled")
        self.othersEntry = tk.Text(contentFrame, height=2, width=25, state="disabled")

        timeLabel = tk.Label(contentFrame, text="Select Time:", font=self.font, bg=self.bg, fg=self.fg)
        self.timeOptions = [f"{hour:02}:{minute:02}" for hour in range(8, 17) for minute in [0, 30]]
        self.timeOptions = [time for time in self.timeOptions if time != "12:00" and time != "12:30"]
        self.timePicker = ttk.Combobox(contentFrame, values=self.timeOptions, width=10, state="readonly")


        #buttonFrame = tk.Frame(contentFrame, bg=self.bg)
        self.clearButton = tk.Button(contentFrame, text="Clear", width=15, activebackground="#DADBB1",
                                     command=self.clearForm)
        self.submitButton = tk.Button(contentFrame, text="Submit", width=15, activebackground="#DADBB1",
                                      command=self.submitData)


        # Layout configuration
        contentFrame.grid(row=0, column=0, sticky="nsew")

        # Title Frame
        titleFrame.grid(row=0, column=0, columnspan=4, pady=(0, 20), sticky="nsew")
        titleLabel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        titleFrame.grid_propagate(False)
        titleFrame.grid_rowconfigure(0, weight=1)
        titleFrame.grid_columnconfigure(0, weight=1)

        # Displaying Widgets using Grid Placement
        studNumLabel.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.studNumEntry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        nameLabel.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.nameEntry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        appTypeLabel.grid(row=3, column=0, padx=10, pady=10, sticky="nw")
        self.appTypeCheckBox.grid(row=3, column=1, padx=10, pady=10, sticky="nw")

        dateLabel.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.dateEntry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        courseLabel.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        self.courseEntry.grid(row=1, column=3, padx=10, pady=10, sticky="w")

        sectionLabel.grid(row=2, column=2, padx=10, pady=10, sticky="w")
        self.sectionEntry.grid(row=2, column=3, padx=10, pady=10, sticky="w")

        self.othersLabel.grid(row=3, column=2, padx=10, pady=10, sticky="nw")
        self.othersEntry.grid(row=3, column=3, padx=10, pady=10, sticky="w")

        timeLabel.grid(row=4, column=2, padx=10, pady=10, sticky="w")
        self.timePicker.grid(row=4, column=3, padx=10, pady=10, sticky="w")

        # Button Frame Layout
        # buttonFrame.grid(row=5, column=1, columnspan=3, pady=20, sticky="nsew")
        self.clearButton.grid(row=5, column=1, padx=(10, 10), pady=35)
        self.submitButton.grid(row=5, column=2, columnspan=2, padx=(20, 10), pady=35, sticky="w")

    def pickDate(self, event):
        dateWindow = tk.Toplevel(self.userPage)
        dateWindow.grab_set()
        dateWindow.title("Select Appointment Date")

        cal = Calendar(dateWindow, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack()

        # Submit button that updates dateEntry with the selected date
        submitButton = tk.Button(
            dateWindow,
            text="Submit",
            command=lambda: [self.grabDate(cal), dateWindow.destroy()]
        )
        submitButton.pack()

    def grabDate(self, cal):
        # Update the dateEntry with the selected date
        selected_date = cal.get_date()
        self.dateEntry.delete(0, tk.END)
        self.dateEntry.insert(0, selected_date)

        # Update time options based on database bookings for the selected date
        self.updateTimePicker(selected_date)

    def updateTimePicker(self, selected_date):
        try:
            # Connect to the MySQL database
            connect = mc.connect(
                host="localhost",
                user="root",  # Replace with your MySQL username
                password="",  # Replace with your MySQL password
                database="oras_trial"
            )
            cursor = connect.cursor()

            # Query to count bookings for each time slot on the selected date
            query = """
            SELECT time, COUNT(*) as booking_count
            FROM user_input_forms
            WHERE date = %s
            GROUP BY time
            """
            cursor.execute(query, (selected_date,))
            results = cursor.fetchall()

            # Create a set of fully booked times
            booked_times = {row[0] for row in results if row[1] >= 3}

            # Update the timePicker options
            available_times = [
                time for time in self.timeOptions if time not in booked_times
            ]
            self.timePicker.config(values=available_times)

            # Clear current selection if no longer valid
            if self.timePicker.get() not in available_times:
                self.timePicker.set("")

        except mc.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if connect.is_connected():
                cursor.close()
                connect.close()

    def toggleOthersEntry(self, event):
        """Enable or disable 'Others' entry based on the selected appointment type."""
        if self.appTypeCheckBox.get() == "Others (Please Specify)":
            self.othersLabel.config(state="normal")  # Enable label
            self.othersEntry.config(state="normal")  # Enable entry
        else:
            self.othersEntry.delete("1.0", "end")  # Clear text if previously enabled
            self.othersLabel.config(state="disabled")  # Disable entry
            self.othersEntry.config(state="disabled")  # Disable entry


    def submitData(self):
        # Get values from the form
        student_number = self.studNumEntry.get()
        name = self.nameEntry.get()
        appointment_type = self.appTypeCheckBox.get()
        date = self.dateEntry.get()
        course = self.courseEntry.get()
        section = self.sectionEntry.get()
        others = self.othersEntry.get("1.0", "end").strip()  # Get multi-line text
        time = self.timePicker.get()

        if appointment_type == "Others (Please Specify)":
            if not others:
                messagebox.showerror("Error", "Please specify the 'Others' field!")
                return
            appointment_type = others

        # Validate the input (example: check required fields)
        if not (student_number.strip() and name.strip() and appointment_type.strip() and course.strip()
                and section.strip() and time.strip()) or date.strip() == "yyyy-mm-dd":
            messagebox.showerror("Error", "All fields except 'Others' are required!")
            return

        # Connect to the MySQL database
        try:
            connect = mc.connect(
                host="localhost",
                user="root",  # Replace with your MySQL username
                password="",  # Replace with your MySQL password
                database="oras_trial"
            )
            cursor = connect.cursor()

            # SQL query to insert data
            insert_query = """
            INSERT INTO user_input_forms(stud_num, name, course, section, appointment_type, date, time)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (student_number, name, course, section, appointment_type, date, time)
            cursor.execute(insert_query, values)

            # Commit the transaction
            connect.commit()

            # Success message
            messagebox.showinfo("Success", "Data submitted successfully!")

            # Clear form after submission
            self.clearForm()

        except mc.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if connect.is_connected():
                cursor.close()
                connect.close()

    def clearForm(self):
        # Clear all form fields
        self.studNumEntry.delete(0, tk.END)
        self.nameEntry.delete(0, tk.END)
        self.appTypeCheckBox.set("")
        self.dateEntry.delete(0, tk.END)
        self.dateEntry.insert(0, " yyyy-mm-dd")
        self.courseEntry.delete(0, tk.END)
        self.sectionEntry.delete(0, tk.END)
        self.othersEntry.delete("1.0", "end")
        self.othersLabel.config(state="disabled")
        self.othersEntry.config(state="disabled")
        self.timePicker.set("")
