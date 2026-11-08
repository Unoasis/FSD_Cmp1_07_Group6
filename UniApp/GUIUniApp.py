import tkinter as tk
from pathlib import Path

from database import Database
from validator import Validator
from gui_errors import show_error


class GUIUniApp:
    def __init__(self):
        # Create the only Tk root window.
        self.root = tk.Tk()
        self.root.title("University Student Login")
        self.root.geometry("420x280")
        self.root.resizable(False, False)

        data_file = Path(__file__).resolve().parent / "students.data"
        self.database = Database(data_file)

        self.create_login_window()

    
    def create_login_window(self):
        tk.Label(
            self.root,
            text="Student Login",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Label(self.root, text="Email:").pack()

        self.email_entry = tk.Entry(self.root, width=35)
        self.email_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack()

        self.password_entry = tk.Entry(
            self.root,
            width=35,
            show="*"
        )
        self.password_entry.pack(pady=5)

        tk.Button(
            self.root,
            text="Login",
            width=15,
            command=self.login
        ).pack(pady=20)

    
    def login(self):
        # Step 1: Get input from the GUI.
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        # Step 2: Check empty fields.
        if not email or not password:
            show_error(self.root, "Email and password cannot be empty.")
            return

        # Step 3: Validate input formats.
        if not Validator.validate_credentials(email, password):
            show_error(self.root, "Incorrect email or password format.")
            return

        # Step 4: Read the latest registered students.
        self.database.load_from_file()

        # Step 5: Find the student and check the password.
        student = self.database.find_student_by_email(email)

        if student is None or not student.login(password):
            show_error(self.root, "Student does not exist.")
            return

        # Step 6: Open the enrolment window.
        self.open_enrolment_window(student)


    def open_enrolment_window(self, student):
        # Import the GUI module provided by the teammate.
        try:
            from gui_enrolment import show_enrolment_window
        except ModuleNotFoundError as exc:
            if exc.name != "gui_enrolment":
                raise
            show_error(self.root, "Enrolment window is not connected yet.")
            return

        # Hide the login window after successful authentication.
        self.root.withdraw()

        try:
            show_enrolment_window(self.root, student, self.database)
        except Exception:
            self.root.deiconify()
            raise


    def run(self):
        self.root.mainloop()

    
if __name__ == "__main__":
    GUIUniApp().run()


