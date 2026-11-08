import tkinter as tk
from tkinter import ttk


class SubjectWindow:

    def __init__(self, parent, student, on_close=None):
        self.student = student
        self.on_close = on_close
        self.window = tk.Toplevel(parent)
        self.window.title("Enrolled Subjects")
        self.window.geometry("540x360")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        frame = ttk.Frame(self.window, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame, text="My Subjects", font=("Arial", 17, "bold")
        ).pack(pady=(0, 8))
        ttk.Label(
            frame,
            text=f"{student.get_name()}  |  Student ID: {student.get_id()}"
        ).pack(pady=(0, 12))

        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True)

        self.table = ttk.Treeview(
            table_frame,
            columns=("id", "mark", "grade"),
            show="headings",
            height=5,
            selectmode="none"
        )
        for column, heading in (
            ("id", "Subject ID"),
            ("mark", "Mark"),
            ("grade", "Grade"),
        ):
            self.table.heading(column, text=heading)
            self.table.column(column, width=155, anchor="center", stretch=True)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.table.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.table.configure(yscrollcommand=scrollbar.set)

        self.empty_text = tk.StringVar()
        ttk.Label(frame, textvariable=self.empty_text, foreground="#666666").pack(pady=(6, 0))

        self.summary_text = tk.StringVar()
        ttk.Label(frame, textvariable=self.summary_text).pack(pady=(4, 12))

        buttons = ttk.Frame(frame)
        buttons.pack()
        ttk.Button(buttons, text="Refresh", command=self.refresh, width=13).pack(
            side="left", padx=6
        )
        ttk.Button(buttons, text="Close", command=self.close_window, width=13).pack(
            side="left", padx=6
        )

        self.refresh()

    def is_open(self):
        return bool(self.window.winfo_exists())

    def refresh(self):
        if not self.is_open():
            return

        for row_id in self.table.get_children():
            self.table.delete(row_id)

        subjects = self.student.get_enrolment_list()
        for subject in subjects:
            self.table.insert("", "end", values=(
                subject.get_subject_id(),
                subject.get_mark(),
                subject.get_grade(),
            ))

        self.empty_text.set("No subjects enrolled yet." if not subjects else "")
        self.summary_text.set(
            f"Total subjects: {len(subjects)}    |    "
            f"Average mark: {self.student.get_average_mark():.2f}"
        )

    def close_window(self):
        if self.is_open():
            self.window.destroy()
        if self.on_close is not None:
            self.on_close()
