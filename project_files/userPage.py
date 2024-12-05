import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import style
import mysql.connector as mc
import qrcode
from PIL import ImageTk
import loginSignup


class UserUI:
    def __init__(self, root, username):
        self.root = tk.Toplevel(root)
        self.root.configure(bg="#54742C")
        self.root.title(f"{username} Appointment Form")
        self.root.geometry("990x500+280+70")
        self.root.resizable(False, False)
        self.root.tk.call('tk', 'scaling', 2.0)
        self.bg = style.labelBgColor
        self.fg = style.labelTextColor
        self.font = style.userFontLabel

        # First method to be executed
        self.userUIContent()


    # User Interface of Admin Window
    def userUIContent(self):
        # Initializing the widgets and frames
        contentFrame = tk.Frame(self.root, bg="#54742C", padx=20, pady=20)  # Darker background (swapped)
        titleFrame = tk.Frame(self.root, bg="#DADBB1", height=100)  # Lighter background (swapped)
        titleLabel = tk.Label(titleFrame, text="ORAS: Office of the Registrar Appointment System",
                              font=("Verdana", 16, "bold"), bg="#DADBB1", fg="#000000")

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
        self.courseCheckBox = ttk.Combobox(contentFrame, values=["ACT", "BLIS", "BSCS", "BSIS", "BSA", "BSE", "BSTM",
                                                                 "BAELS", "BPEd", "BSMath", "BSNE", "BSP", "BTVTED" ],
                                                                  width=28, state="readonly")


        sectionLabel = tk.Label(contentFrame, text="Section:", font=self.font, bg=self.bg, fg=self.fg)
        self.sectionEntry = tk.Entry(contentFrame, width=30)

        self.othersLabel = tk.Label(contentFrame, text="Others:", font=self.font, bg=self.bg, fg=self.fg,
                               disabledforeground="#3b3b3b" , state="disabled")
        self.othersEntry = tk.Text(contentFrame, height=2, width=25, state="disabled")

        timeLabel = tk.Label(contentFrame, text="Select Time:", font=self.font, bg=self.bg, fg=self.fg)
        self.timeOptions = [f"{hour:02}:{minute:02}" for hour in range(8, 17) for minute in [0, 30]]
        self.timeOptions = [time for time in self.timeOptions if time != "12:00" and time != "12:30"]
        self.timePicker = ttk.Combobox(contentFrame, values=self.timeOptions, width=10, state="readonly")


        self.clearButton = tk.Button(contentFrame, text="Clear", width=15, activebackground="#DADBB1",
                                     command=self.clearForm)
        self.submitButton = tk.Button(contentFrame, text="Submit", width=15, activebackground="#DADBB1",
                                      command=self.submitData)

        # Logout Button
        logoutButton = tk.Button(contentFrame, text="Log out", font=("Arial", 8), bg=style.accFrameColor,
                                 fg=style.accFgColor, activebackground=style.accFontColor, bd=0, command=self.logout)


        # Displaying of widgets and frames
        # Title Frame
        titleFrame.grid(row=0, column=0, columnspan=4, pady=(0, 20), sticky="nsew")
        titleLabel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        titleFrame.grid_propagate(False)
        titleFrame.grid_rowconfigure(0, weight=1)
        titleFrame.grid_columnconfigure(0, weight=1)

        # Content Frame
        contentFrame.grid(row=1, column=0, sticky="nsew")

        studNumLabel.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.studNumEntry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        nameLabel.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.nameEntry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        appTypeLabel.grid(row=3, column=0, padx=10, pady=10, sticky="nw")
        self.appTypeCheckBox.grid(row=3, column=1, padx=10, pady=10, sticky="nw")

        dateLabel.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.dateEntry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        courseLabel.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        self.courseCheckBox.grid(row=1, column=3, padx=10, pady=10, sticky="w")

        sectionLabel.grid(row=2, column=2, padx=10, pady=10, sticky="w")
        self.sectionEntry.grid(row=2, column=3, padx=10, pady=10, sticky="w")

        self.othersLabel.grid(row=3, column=2, padx=10, pady=10, sticky="nw")
        self.othersEntry.grid(row=3, column=3, padx=10, pady=10, sticky="w")

        timeLabel.grid(row=4, column=2, padx=10, pady=10, sticky="w")
        self.timePicker.grid(row=4, column=3, padx=10, pady=10, sticky="w")

        self.clearButton.grid(row=5, column=1, padx=(10, 10), pady=(35,25))
        self.submitButton.grid(row=5, column=2, columnspan=2, padx=(20, 10), pady=(35,25), sticky="w")

        logoutButton.grid(row=6, column=3, sticky="e", padx=10)


    # Method for Calendar
    def pickDate(self, event):
        dateWindow = tk.Toplevel(self.root)
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


    # Method for getting/displaying the date
    def grabDate(self, cal):
        # Update the dateEntry with the selected date
        selected_date = cal.get_date()
        self.dateEntry.delete(0, tk.END)
        self.dateEntry.insert(0, selected_date)

        # Update time options based on database bookings for the selected date
        self.updateTimePicker(selected_date)


    # Method for updating the time and removing when picked three times
    def updateTimePicker(self, selected_date):
        try:
            # Connect to the MySQL database
            connect = mc.connect(host="localhost", user="root", password="", database="oras_trial")
            cursor = connect.cursor()

            # Query to count bookings for each time slot on the selected date
            query = "SELECT time, COUNT(*) as booking_count FROM user_input_forms WHERE date = %s GROUP BY time"
            cursor.execute(query, (selected_date,))
            results = cursor.fetchall()

            # 3 times == fully booked
            booked_times = {row[0] for row in results if row[1] >= 3}

            available_times = [
                time for time in self.timeOptions if time not in booked_times
            ]
            self.timePicker.config(values=available_times)

            if self.timePicker.get() not in available_times:
                self.timePicker.set("")

        except mc.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if connect.is_connected():
                cursor.close()
                connect.close()


    # Method to enable or disable 'Others' entry based on the selected appointment type
    def toggleOthersEntry(self, event):
        if self.appTypeCheckBox.get() == "Others (Please Specify)":
            self.othersLabel.config(state="normal")
            self.othersEntry.config(state="normal")
        else:
            self.othersEntry.delete("1.0", "end")
            self.othersLabel.config(state="disabled")
            self.othersEntry.config(state="disabled")


    # Method for submitting data to the database
    def submitData(self):
        # Get values from the form
        student_number = self.studNumEntry.get()
        name = self.nameEntry.get()
        appointment_type = self.appTypeCheckBox.get()
        date = self.dateEntry.get()
        course = self.courseCheckBox.get()
        section = self.sectionEntry.get()
        others = self.othersEntry.get("1.0", "end").strip()  # Get multi-line text
        time = self.timePicker.get()

        # Validate the input and every field should be filled out
        if not (student_number.strip() and name.strip() and appointment_type.strip() and course.strip()
                and section.strip() and time.strip()) or date.strip() == "yyyy-mm-dd":
            messagebox.showerror("Error", "All fields except 'Others' are required!")
            return

        if len(student_number) != 7:
            messagebox.showerror("Error", "Student number must be 7 characters long in the format XX-XXXX")
            return

        if student_number[2] != "-":
            messagebox.showerror("Error", "The correct student number format should be XX-XXXX")
            return

        if appointment_type == "Others (Please Specify)":
            if not others:
                messagebox.showerror("Error", "Please specify the 'Others' field!")
                return
            appointment_type = others


        # Connect to the MySQL database
        try:
            connect = mc.connect(host="localhost", user="root", password="", database="oras_trial")
            cursor = connect.cursor()

            # SQL query to insert data (used """ for multiline strings)
            insert_query = """
            INSERT INTO user_input_forms(stud_num, name, course, section, appointment_type, date, time)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (student_number, name, course, section, appointment_type, date, time)
            cursor.execute(insert_query, values)
            connect.commit()

            messagebox.showinfo("Success", "Data submitted successfully!")

            # Generate and display the QR code in a new window
            self.generateQRCode(student_number)

            # Clear form after submission
            self.clearForm()

        except mc.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if connect.is_connected():
                cursor.close()
                connect.close()


    # Method to generate QR Code
    def generateQRCode(self, student_number):
        # Generate QR code from the student number
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(student_number)
        qr.make(fit=True)

        # Create an image from the QR code
        img = qr.make_image(fill="black", back_color="white")

        # Convert to a format that can be used in tkinter
        img_tk = ImageTk.PhotoImage(img)

        # Create a new window to display the QR code
        qr_window = tk.Toplevel(self.root)
        qr_window.title("QR Code")
        qr_window.geometry("300x300")

        # Label to display the QR code image
        qr_label = tk.Label(qr_window, image=img_tk)
        qr_label.image = img_tk
        qr_label.pack(padx=20, pady=20)


    # Method used to clear the form
    def clearForm(self):
        # Clear all form fields
        self.studNumEntry.delete(0, tk.END)
        self.nameEntry.delete(0, tk.END)
        self.appTypeCheckBox.set("")
        self.dateEntry.delete(0, tk.END)
        self.dateEntry.insert(0, " yyyy-mm-dd")
        self.courseCheckBox.set("")
        self.sectionEntry.delete(0, tk.END)
        self.othersEntry.delete("1.0", "end")
        self.othersLabel.config(state="disabled")
        self.othersEntry.config(state="disabled")
        self.timePicker.set("")


    # Method used to Log out
    def logout(self):
        confirm = messagebox.askyesno("Logout Confirmation", "Are you sure you want to log out?")

        if confirm:
            self.root.withdraw()
            loginPage = loginSignup.LoginSignUp(self.root)
            self.root.deiconify()
