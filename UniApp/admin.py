"""Admin model class - Assessment 1 Part 2&3, Task (d)

Admin(Person) is the model class of the Admin System. It realises the admin
backlog items:

    admin_access()          701  admin subsystem needs no registration
    view_all_students()     502  read every student from students.data
    group_by_grade()        702  group students by grade
    categorise_pass_fail()  703  partition students into PASS / FAIL
    remove_student()        704  remove one student by ID
    clear_all_students()    705  clear students.data

Admin has no fields of its own (the identity fields are inherited from
Person) and depends on Database, which is passed in to each operation rather
than stored, so the relationship stays a dependency as in the Part 1 class
diagram.

This class contains no input() or print() calls. All menu handling and output
lives in AdminController (admin_controller.py).
"""

from person import Person
from subject import Subject

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