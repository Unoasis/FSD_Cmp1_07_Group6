"""AdminController - Assessment 1 Part 2&3, Task (d)

Controller class of the Admin System. It drives the menu and prints the output,
using the Admin class to do the work. Menu actions:

    (c) clear database     - clear all data on students.data
    (g) group students     - group students by grade
    (p) partition students - partition students into PASS/FAIL
    (r) remove student     - remove a student by ID
    (s) show               - show all students
    (x) exit               - return to the university menu

Every action reads from or writes to students.data through the Database class.
Output wording and indentation follow the sample I/O exactly.
"""

from admin import Admin
from database import Database

# One tab of indentation under the university menu, as in the sample I/O.
TAB = "\t"

# Grade order used when printing the grade grouping. The sample shows P
# before C, i.e. groups are listed from the lowest band upwards.
GRADE_ORDER = ["Z", "P", "C", "D", "HD"]


class AdminController:
    """Drives the admin subsystem menu and prints the output."""

    CYAN = "\033[36m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    RESET = "\033[0m"

    def __init__(self, database=None, admin=None):
        self.database = database if database is not None else Database()
        self.admin = admin if admin is not None else Admin()

    # ------------------------------------------------------------------
    # Menu loop
    # ------------------------------------------------------------------

    def run(self):
        """Show the admin menu until the admin chooses (x) exit."""
        if not self.admin.admin_access():
            self.print_error("Admin access denied.")
            return

        while True:
            try:
                choice = input(
                    f"{TAB}{self.CYAN}Admin System (c/g/p/r/s/x): {self.RESET}"
                ).strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                return

            if choice == "c":
                self.clear_database()
            elif choice == "g":
                self.group_students()
            elif choice == "p":
                self.partition_students()
            elif choice == "r":
                self.remove_student()
            elif choice == "s":
                self.show_students()
            elif choice == "x":
                return
            else:
                self.print_error("Invalid option. Please choose c, g, p, r, s or x.")

    # ------------------------------------------------------------------
    # (s) Show all students
    # ------------------------------------------------------------------

    def show_students(self):
        self.print_info("Student List")

        students = self.admin.view_all_students(self.database)
        if not students:
            self.print_nothing_to_display()
            return

        for student in students:
            print(
                f"{TAB}{student.get_name()} :: {student.get_id()} "
                f"--> Email: {student.get_email()}"
            )

    # ------------------------------------------------------------------
    # (g) Group students by grade
    # ------------------------------------------------------------------

    def group_students(self):
        self.print_info("Grade Grouping")

        groups = self.admin.group_by_grade(self.database)
        if not groups:
            self.print_nothing_to_display()
            return

        # Known grades first, in band order, then anything unexpected.
        ordered = [g for g in GRADE_ORDER if g in groups]
        ordered += [g for g in groups if g not in GRADE_ORDER]

        for grade in ordered:
            entries = ", ".join(
                self.format_with_grade(student) for student in groups[grade]
            )
            print(f"{TAB}{grade:<2} --> [{entries}]")

    # ------------------------------------------------------------------
    # (p) Partition students into PASS / FAIL
    # ------------------------------------------------------------------

    def partition_students(self):
        self.print_info("PASS/FAIL Partition")

        passed, failed = self.admin.categorise_pass_fail(self.database)

        # Note: unlike show/group, the sample prints empty brackets here when
        # the database is empty rather than "< Nothing to Display >".
        print(f"{TAB}FAIL --> [{self.format_list(failed)}]")
        print(f"{TAB}PASS --> [{self.format_list(passed)}]")

    # ------------------------------------------------------------------
    # (r) Remove a student by ID
    # ------------------------------------------------------------------

    def remove_student(self):
        try:
            student_id = input(f"{TAB}Remove by ID: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return

        if not student_id:
            self.print_error("Student ID cannot be empty")
            return

        if not student_id.isdigit():
            self.print_error(f"Student {student_id} does not exist")
            return

        try:
            removed = self.admin.remove_student(self.database, student_id)
        except (OSError, ValueError):
            self.print_error("Unable to update students.data")
            return

        if removed is None:
            self.print_error(f"Student {student_id} does not exist")
            return

        self.print_info(f"Removing Student {removed.get_id()} Account")

    # ------------------------------------------------------------------
    # (c) Clear the database
    # ------------------------------------------------------------------

    def clear_database(self):
        self.print_info("Clearing students database")

        while True:
            try:
                confirm = input(
                    f"{TAB}{self.RED}"
                    f"Are you sure you want to clear the database (Y)ES/(N)O: "
                    f"{self.RESET}"
                ).strip().upper()
            except (EOFError, KeyboardInterrupt):
                print()
                return

            if confirm == "Y":
                try:
                    self.admin.clear_all_students(self.database)
                except (OSError, ValueError):
                    self.print_error("Unable to clear students.data")
                    return

                self.print_info("Students data cleared")
                return

            if confirm == "N":
                return

            self.print_error("Please answer Y or N")

    # ------------------------------------------------------------------
    # Formatting helpers
    # ------------------------------------------------------------------

    def format_with_grade(self, student):
        """'Alen Jones :: 762740 --> GRADE:  P - MARK: 63.50'

        Two spaces after 'GRADE:' and a two-decimal mark, matching the sample.
        """
        return (
            f"{student.get_name()} :: {student.get_id()} --> "
            f"GRADE:  {Admin.get_grade(student)} - "
            f"MARK: {student.get_average_mark():.2f}"
        )

    def format_list(self, students):
        return ", ".join(self.format_with_grade(student) for student in students)

    def print_info(self, message):
        print(f"{TAB}{self.YELLOW}{message}{self.RESET}")

    def print_error(self, message):
        print(f"{TAB}{self.RED}{message}{self.RESET}")

    def print_nothing_to_display(self):
        print(f"{TAB}{TAB}< Nothing to Display >")


def admin_menu(database):
    """Entry point used by CLIUniApp to open the admin subsystem."""
    AdminController(database).run()


if __name__ == "__main__":
    test_database = Database("test_students.data")
    admin_menu(test_database)