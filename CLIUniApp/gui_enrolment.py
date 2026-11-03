import tkinter as tk
from tkinter import ttk

from gui_errors import show_error
from gui_subjects import SubjectWindow


class EnrolmentWindow:

    def __init__(self, root, student, database):
        self.root = root                    
        self.student = student              
        self.database = database             
        self.subject_view = None            
        self.window = tk.Toplevel(root)
        self.window.title("Student Enrolment")
        self.window.geometry("500x330")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        self.build_interface()
        self.refresh_count()

    def build_interface(self):
        frame = ttk.Frame(self.window, padding=25)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame, text="Student Enrolment", font=("Arial", 18, "bold")
        ).pack(pady=(0, 14))

        ttk.Label(
            frame, text=f"Welcome, {self.student.get_name()}!"
        ).pack(pady=3)
        ttk.Label(
            frame, text=f"Student ID: {self.student.get_id()}"
        ).pack(pady=3)

        self.count_text = tk.StringVar()
        ttk.Label(frame, textvariable=self.count_text).pack(pady=(18, 5))

        self.progress = ttk.Progressbar(
            frame, maximum=self.student.MAX_SUBJECTS, length=300
        )
        self.progress.pack(pady=(0, 10))

        self.status_text = tk.StringVar(value="Click Enrol to add a subject.")
        ttk.Label(frame, textvariable=self.status_text, foreground="#24618a").pack(
            pady=(0, 13)
        )

        buttons = ttk.Frame(frame)
        buttons.pack()

        ttk.Button(buttons, text="Enrol", command=self.enrol, width=15).grid(
            row=0, column=0, padx=5, pady=3
        )
        ttk.Button(
            buttons, text="Show Subjects", command=self.show_subjects, width=15
        ).grid(row=0, column=1, padx=5, pady=3)
        ttk.Button(buttons, text="Logout", command=self.close_window, width=15).grid(
            row=0, column=2, padx=5, pady=3
        )

    def refresh_count(self):
        count = len(self.student.get_enrolment_list())
        limit = self.student.MAX_SUBJECTS
        self.count_text.set(f"Currently enrolled: {count} / {limit} subjects")
        self.progress.configure(value=count)

    def enrol(self):
        new_subject = self.student.enrol_subject()

        if new_subject is None:
            show_error(
                self.window,
                f"Students are allowed to enrol in {self.student.MAX_SUBJECTS} subjects only."
            )
            return


        try:
            saved = self.database.update_student(self.student)
        except (OSError, ValueError):
            saved = False

        if not saved:
            self.student.remove_subject(new_subject.get_subject_id())
            self.refresh_count()
            show_error(self.window, "Unable to save enrolment to students.data.")
            return

        self.status_text.set(
            f"Enrolled in Subject-{new_subject.get_subject_id()} successfully."
        )
        self.refresh_count()


        if self.subject_view is not None and self.subject_view.is_open():
            self.subject_view.refresh()

    def show_subjects(self):
        if self.subject_view is not None and self.subject_view.is_open():
            self.subject_view.refresh()
            self.subject_view.window.lift()
            self.subject_view.window.focus_set()
            return

        self.subject_view = SubjectWindow(
            parent=self.window,
            student=self.student,
            on_close=self._subject_window_closed,
        )

    def _subject_window_closed(self):
        self.subject_view = None

    def close_window(self):
        """Logout or X: close child windows and return to Login Window."""
        if self.subject_view is not None and self.subject_view.is_open():
            self.subject_view.close_window()

        self.window.destroy()
        self.root.deiconify()
        self.root.lift()


def show_enrolment_window(root, student, database):
    
    return EnrolmentWindow(root, student, database)
