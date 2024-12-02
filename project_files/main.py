import tkinter as tk
from project_files import loginSignup as logSign

# Main Activity
root = tk.Tk()
loginSignUp = logSign.LoginSignUp(root)
root.mainloop()