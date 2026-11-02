from student import Student
from validator import Validator



class SubjectController:
    CYAN = "\033[36m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    RESET = "\033[0m"
    INDENT = "\t\t"

    def __init__(self, student, database):
        self._student = student
        self._database = database

    def run(self):
        """Show the Student Course Menu until the student enters x."""
        while True:
            choice = input(
                f"{self.INDENT}{self.CYAN}Student Course Menu (c/e/r/s/x): "
                f"{self.RESET}"
            ).strip().lower()

            if choice == "c":
                self.change_password()
            elif choice == "e":
                self.enrol_subject()
            elif choice == "r":
                self.remove_subject()
            elif choice == "s":
                self.show_subjects()
            elif choice == "x":
                return
            else:
                self.print_error("Invalid option. Please enter c, e, r, s or x.")

    def change_password(self):
        self.print_info("Updating Password")
        new_password = input(f"{self.INDENT}New Password: ")
        while not Validator.validate_password(new_password):
            self.print_error("Incorrect password format")
            new_password = input(f"{self.INDENT}New Password: ")

        confirm_password = input(f"{self.INDENT}Confirm Password: ")
        while confirm_password != new_password:
            self.print_error("Password does not match - try again")
            confirm_password = input(f"{self.INDENT}Confirm Password: ")
        self._student.update_password(new_password)
        self.save()

    def enrol_subject(self):
        new_subject = self._student.enrol_subject()
        if new_subject is None:
            self.show_enrolment_limit_error()
            return
        self.save()
        self.print_info(f"Enrolling in Subject-{new_subject.get_subject_id()}")
        self.show_enrolment_count()

    def show_enrolment_limit_error(self):
        self.print_error(f"Students are allowed to enrol in {Student.MAX_SUBJECTS} subjects only")

    def remove_subject(self):
        subject_id = input(f"{self.INDENT}Remove Subject by ID: ").strip()

        try:
            subject_id = str(int(subject_id)).zfill(3)
        except ValueError:
            self.print_error("Subject ID must be a number")
            return

        if self._student.remove_subject(subject_id):
            self.save()
            self.print_info(f"Dropping Subject-{subject_id}")
            self.show_enrolment_count()
        else:
            self.print_error(f"Subject-{subject_id} does not exist")

    def show_subjects(self):
        subjects = self._student.view_enrolment()
        self.print_info(f"Showing {len(subjects)} subjects")
        for subject in subjects:
            print(f"{self.INDENT}{subject}")

    def show_enrolment_count(self):
        count = len(self._student.get_enrolment_list())
        self.print_info(f"You are now enrolled in {count} out of {Student.MAX_SUBJECTS} subjects")

    def save(self):
        self._database.update_student(self._student)

    def print_info(self, message):
        print(f"{self.INDENT}{self.YELLOW}{message}{self.RESET}")

    def print_error(self, message):
        print(f"{self.INDENT}{self.RED}{message}{self.RESET}")

if __name__ == "__main__":
    from database import Database

    test_database = Database("test_students.data")
    test_student = test_database.find_student_by_email("john.smith@university.com")

    if test_student is None:
        test_student = Student("673358", "John Smith", "john.smith@university.com", "Helloworld123")
        test_database.add_student(test_student)

    SubjectController(test_student, test_database).run()