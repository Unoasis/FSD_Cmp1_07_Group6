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

from models.database import Database
from utils.colours import Colours
 
# One tab of indentation under the university menu, as in the sample I/O.
TAB = "\t"
 
# Grade order used when printing the grade grouping. The sample shows P
# before C, i.e. groups are listed from the lowest band upwards.
GRADE_ORDER = ["Z", "P", "C", "D", "HD"]
 
 
class AdminController:
    """Drives the admin subsystem menu."""
 
    def __init__(self, database=None):
        self.database = database or Database()
 
    # ------------------------------------------------------------------
    # Menu loop
    # ------------------------------------------------------------------
 
    def run(self):
        """Show the admin menu until the admin chooses (x) exit."""
        while True:
            try:
                choice = input(
                    f"{TAB}{Colours.cyan('Admin System (c/g/p/r/s/x): ')}"
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
                print(f"{TAB}{Colours.red('Invalid option. Please choose c, g, p, r, s or x.')}")
 
    # ------------------------------------------------------------------
    # (s) Show all students
    # ------------------------------------------------------------------
 
    def show_students(self):
        print(f"{TAB}{Colours.yellow('Student List')}")
 
        students = self.database.read_students()
        if not students:
            print(f"{TAB}{TAB}{Colours.white('< Nothing to Display >')}")
            return
 
        for student in students:
            print(f"{TAB}{student.name} :: {student.id} --> Email: {student.email}")
 
    # ------------------------------------------------------------------
    # (g) Group students by grade
    # ------------------------------------------------------------------
 
    def group_students(self):
        print(f"{TAB}{Colours.yellow('Grade Grouping')}")
 
        students = self.database.read_students()
        if not students:
            print(f"{TAB}{TAB}{Colours.white('< Nothing to Display >')}")
            return
 
        groups = {}
        for student in students:
            groups.setdefault(student.grade, []).append(self._format_with_grade(student))
 
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
        print(f"{TAB}{Colours.yellow('PASS/FAIL Partition')}")
 
        students = self.database.read_students()
 
        failed = [self._format_with_grade(s) for s in students if not s.is_pass]
        passed = [self._format_with_grade(s) for s in students if s.is_pass]
 
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
            print(f"{TAB}{Colours.red('Student ID cannot be empty')}")
            return
 
        if not student_id.isdigit():
            print(f"{TAB}{Colours.red(f'Student {student_id} does not exist')}")
            return
 
        # Accept "12345" for a stored id of "012345" without losing the
        # padded form the sample output uses.
        padded_id = student_id.zfill(6)
        target = self.database.get_student_by_id(student_id) or self.database.get_student_by_id(padded_id)
 
        if target is None:
            print(f"{TAB}{Colours.red(f'Student {student_id} does not exist')}")
            return
 
        print(f"{TAB}{Colours.red(f'Removing Student {target.id} Account')}")
        if not self.database.remove_student(target.id):
            print(f"{TAB}{Colours.red('Unable to update students.data')}")
 
    # ------------------------------------------------------------------
    # (c) Clear the database
    # ------------------------------------------------------------------
 
    def clear_database(self):
        print(f"{TAB}{Colours.yellow('Clearing students database')}")
 
        while True:
            try:
                confirm = input(
                    f"{TAB}{Colours.red('Are you sure you want to clear the database (Y)ES/(N)O: ')}"
                ).strip().upper()
            except (EOFError, KeyboardInterrupt):
                print()
                return
 
            if confirm == "Y":
                if self.database.clear_all():
                    print(f"{TAB}{Colours.white('Students data cleared')}")
                else:
                    print(f"{TAB}{Colours.red('Unable to clear students.data')}")
                return
 
            if confirm == "N":
                return
 
            print(f"{TAB}{Colours.red('Please answer Y or N')}")
 
    # ------------------------------------------------------------------
    # Formatting helpers
    # ------------------------------------------------------------------
 
    @staticmethod
    def _format_with_grade(student):
        """'Alen Jones :: 762740 --> GRADE:  P - MARK: 63.50'
 
        Two spaces after 'GRADE:' and a two-decimal mark, matching the sample.
        """
        return (
            f"{student.name} :: {student.id} --> "
            f"GRADE:  {student.grade} - MARK: {student.mark:.2f}"
        )
