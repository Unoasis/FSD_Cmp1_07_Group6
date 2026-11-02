"""The Admin System - Assessment 1 Part 2&3, Task (d)

Menu actions (based on the description given):
    (c) clear database     - clear all data on students.data
    (g) group students     - group students by grade
    (p) partition students - partition students into PASS/FAIL
    (r) remove student     - remove a student by ID
    (s) show               - show all students
    (x) exit               - return to the university menu

Every action reads from or writes to students.data through the Database class.
Output wording and indentation follow the sample I/O exactly.
"""

from database import Database
from subject import Subject

# One tab of indentation under the university menu, as in the sample I/O.
TAB = "\t"

# Grade order used when printing the grade grouping. The sample shows P
# before C, i.e. groups are listed from the lowest band upwards.
GRADE_ORDER = ["Z", "P", "C", "D", "HD"]

# A student passes when the average mark of their subjects is 50 or above.
PASS_MARK = 50


class AdminController:
    """Drives the admin subsystem menu."""

    CYAN = "\033[36m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    RESET = "\033[0m"

    def __init__(self, database=None):
        self.database = database if database is not None else Database()

    # ------------------------------------------------------------------
    # Menu loop
    # ------------------------------------------------------------------

    def run(self):
        """Show the admin menu until the admin chooses (x) exit."""
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

        students = self.read_students()
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

        students = self.read_students()
        if not students:
            self.print_nothing_to_display()
            return

        groups = {}
        for student in students:
            grade = self.get_grade(student)
            groups.setdefault(grade, []).append(self.format_with_grade(student))

        # Known grades first, in band order, then anything unexpected.
        ordered = [g for g in GRADE_ORDER if g in groups]
        ordered += [g for g in groups if g not in GRADE_ORDER]

        for grade in ordered:
            entries = ", ".join(groups[grade])
            print(f"{TAB}{grade:<2} --> [{entries}]")

    # ------------------------------------------------------------------
    # (p) Partition students into PASS / FAIL
    # ------------------------------------------------------------------

    def partition_students(self):
        self.print_info("PASS/FAIL Partition")

        students = self.read_students()

        failed = []
        passed = []

        for student in students:
            if self.has_passed(student):
                passed.append(self.format_with_grade(student))
            else:
                failed.append(self.format_with_grade(student))

        # Note: unlike show/group, the sample prints empty brackets here when
        # the database is empty rather than "< Nothing to Display >".
        print(f"{TAB}FAIL --> [{', '.join(failed)}]")
        print(f"{TAB}PASS --> [{', '.join(passed)}]")

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

        # Accept "12345" for a stored id of "012345" without losing the
        # padded form the sample output uses.
        padded_id = student_id.zfill(6)

        # Read the current file contents before looking the student up.
        students = self.read_students()

        target = self.database.find_student(student_id)
        if target is None:
            target = self.database.find_student(padded_id)

        if target is None:
            self.print_error(f"Student {student_id} does not exist")
            return

        remaining = []
        for student in students:
            if student.get_id() != target.get_id():
                remaining.append(student)

        if self.write_students(remaining):
            self.print_info(f"Removing Student {target.get_id()} Account")
        else:
            self.print_error("Unable to update students.data")

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
                if self.write_students([]):
                    self.print_info("Students data cleared")
                else:
                    self.print_error("Unable to clear students.data")
                return

            if confirm == "N":
                return

            self.print_error("Please answer Y or N")

    # ------------------------------------------------------------------
    # Data helpers
    # ------------------------------------------------------------------

    def read_students(self):
        """Re-read the Student objects from students.data.

        The brief requires the admin system to read from the file when
        listing, grouping and partitioning, so the data is reloaded rather
        than trusting whatever is already in memory.
        """
        self.database.load_from_file()
        return self.database.get_all_students()

    def write_students(self, students):
        """Save `students` as the new contents of students.data.

        Database has add_student() and update_student() but no method for
        removing or clearing, and database.py belongs to another team member,
        so the admin system replaces the student list the Database is holding
        and asks it to save. The file itself is still only ever written by
        Database.save_to_file(), so students.data keeps a single writer.
        """
        try:
            self.database._students = students
            self.database.save_to_file()
            return True
        except (OSError, ValueError):
            return False

    @staticmethod
    def get_grade(student):
        """Grade of a student, worked out from their average mark."""
        return Subject.grade_from_mark(student.get_average_mark())

    @staticmethod
    def has_passed(student):
        return student.get_average_mark() >= PASS_MARK

    # ------------------------------------------------------------------
    # Formatting helpers
    # ------------------------------------------------------------------

    def format_with_grade(self, student):
        """'Alen Jones :: 762740 --> GRADE:  P - MARK: 63.50'

        Two spaces after 'GRADE:' and a two-decimal mark, matching the sample.
        """
        return (
            f"{student.get_name()} :: {student.get_id()} --> "
            f"GRADE:  {self.get_grade(student)} - "
            f"MARK: {student.get_average_mark():.2f}"
        )

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
