import tkinter as tk


def show_enrolment_window(root, student, database):
    # Create a new window connected to the existing root.
    window = tk.Toplevel(root)
    window.title("Student Enrolment")

    # When closing, return to the login window.
    def close_window():
        window.destroy()
        root.deiconify()

    window.protocol("WM_DELETE_WINDOW", close_window)

    # Teammate implements the enrolment interface here.
