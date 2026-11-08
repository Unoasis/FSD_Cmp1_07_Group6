"""The Admin System - Assessment 1 Part 2&3, Task (d)

Structure follows the Part 1 class diagram:

    Admin(Person)    - model class. Realises the admin backlog items:
                       admin_access() 701, view_all_students() 502,
                       group_by_grade() 702, categorise_pass_fail() 703,
                       remove_student() 704, clear_all_students() 705.
                       Admin has no fields of its own (the identity fields
                       are inherited from Person) and depends on Database,
                       which is passed in to each operation rather than
                       stored, so the relationship stays a dependency.

    AdminController  - drives the menu and prints. Menu actions:
                       (c) clear database     - clear all data on students.data
                       (g) group students     - group students by grade
                       (p) partition students - partition students into PASS/FAIL
                       (r) remove student     - remove a student by ID
                       (s) show               - show all students
                       (x) exit               - return to the university menu

Every action reads from or writes to students.data through the Database class.
Output wording and indentation follow the sample I/O exactly.
"""

from person import Person
from database import Database
from subject import Subject

# One tab of indentation under the university menu, as in the sample I/O.
TAB = "\t"

# Grade order used when printing the grade grouping. The sample shows P
# before C, i.e. groups are listed from the lowest band upwards.
GRADE_ORDER = ["Z", "P", "C", "D", "HD"]

# A student passes when the average mark of their subjects is 50 or above.
PASS_MARK = 50


class Admin(Person):
    """Admin model class.

    Admins already exist in the system and never register, so no Admin
    record is written to students.data. Database is received as a method
    parameter so that Admin keeps no fields of its own, matching the
    Part 1 class diagram.
    """

    DEFAULT_NAME = "Admin"
    DEFAULT_EMAIL = "admin@university.com"

    def __init__(self, name=DEFAULT_NAME, email=DEFAULT_EMAIL, password=""):
        Person.__init__(self, name, email, password)

    # ------------------------------------------------------------------
    # Backlog 701 - access the admin subsystem without registering
    # ------------------------------------------------------------------

    def admin_access(self):
        """Admins need no login, so access is always granted."""
        return True

    # ------------------------------------------------------------------
    # Backlog 502 - view all registered students
    # ------------------------------------------------------------------

    def view_all_students(self, database):
        """Read the Student objects from students.data.

        The brief requires the admin system to read from the file when
        listing, grouping and partitioning, so the data is reloaded rather
        than trusting whatever is already in memory.
        """
        database.load_from_file()
        return database.get_all_students()

    # ------------------------------------------------------------------
    # Backlog 702 - group students by grade
    # ------------------------------------------------------------------

    def group_by_grade(self, database):
        """Return {grade: [Student, ...]} for every student on file."""
        groups = {}

        for student in self.view_all_students(database):
            grade = Admin.get_grade(student)
            groups.setdefault(grade, []).append(student)

        return groups

    # ------------------------------------------------------------------
    # Backlog 703 - categorise students into PASS / FAIL
    # ------------------------------------------------------------------

    def categorise_pass_fail(self, database):
        """Return (passed, failed) lists of Students."""
        passed = []
        failed = []

        for student in self.view_all_students(database):
            if Admin.has_passed(student):
                passed.append(student)
            else:
                failed.append(student)

        return passed, failed

    # ------------------------------------------------------------------
    # Backlog 704 - remove an individual student
    # ------------------------------------------------------------------

    def remove_student(self, database, student_id):
        """Remove one student from students.data.

        Returns the Student that was removed, or None when no student has
        that ID. A plain "12345" is accepted for a stored ID of "012345".
        """
        students = self.view_all_students(database)

        target = database.find_student(student_id)
        if target is None:
            target = database.find_student(str(student_id).zfill(6))

        if target is None:
            return None

        remaining = []
        for student in students:
            if student.get_id() != target.get_id():
                remaining.append(student)

        Admin.save_students(database, remaining)
        return target

    # ------------------------------------------------------------------
    # Backlog 705 - clear all student records
    # ------------------------------------------------------------------

    def clear_all_students(self, database):
        """Empty students.data."""
        Admin.save_students(database, [])

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def save_students(database, students):
        """Save `students` as the new contents of students.data.

        Database has add_student() and update_student() but no method for
        removing or clearing, so the admin system replaces the student list
        the Database is holding and asks it to save. The file itself is
        still only ever written by Database.save_to_file(), so students.data
        keeps a single writer.
        """
        database._students = students
        database.save_to_file()

    @staticmethod
    def get_grade(student):
        """Grade of a student, worked out from their average mark."""
        return Subject.grade_from_mark(student.get_average_mark())

    @staticmethod
    def has_passed(student):
        return student.get_average_mark() >= PASS_MARK


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