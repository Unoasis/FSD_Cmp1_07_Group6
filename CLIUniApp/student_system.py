
from student import Student
from validator import Validator
from subject_controller import SubjectController


# Terminal text colours
CYAN = "\033[36m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"
GREEN = "\033[32m"

TAB = "\t"


def student_menu(database):
    while True:
        choice = input(TAB + CYAN + "Student System (l/r/x): " + RESET).strip().lower()

        if choice == "l":
            student = login_account(database)

            if student is not None:
                subject_controller = SubjectController(student, database)
                subject_controller.run()

        elif choice == "r":
            register_account(database)

        elif choice == "x":
            return

        else:
            print(TAB + RED + "Invalid option" + RESET)


def register_account(database):
    print(TAB + GREEN + "Student Sign Up" + RESET)

    while True:
        email = input(TAB + "Email: ")
        password = input(TAB + "Password: ")

        if not Validator.validate_credentials(email, password):
            print(TAB + RED + "Incorrect email or password format" + RESET)
            continue

        print(TAB + YELLOW + "email and password formats acceptable" + RESET)
        break

    existing_student = database.find_student_by_email(email)

    if existing_student is not None:
        print(f"{TAB}{RED}Student {existing_student.get_name()} already exists{RESET}")
        return

    name = input("Name: ")

    existing_ids = [
        student.get_id()
        for student in database.get_all_students()
    ]

    student_id = Validator.generate_ID(existing_ids)

    new_student = Student(student_id, name, email, password)

    success = database.add_student(new_student)

    if success:
        print(f"{TAB}{YELLOW}Enrolling Student {name}{RESET}")
    else:
        print(TAB + RED + "Student registration failed" + RESET)


def login_account(database):
    print(TAB + GREEN + "Student Sign In" + RESET)

    while True:
        email = input(TAB + "Email: ")
        password = input(TAB + "Password: ")

        if not Validator.validate_credentials(email, password):
            print(TAB + RED + "Incorrect email or password format" + RESET)
            continue

        print(TAB + YELLOW + "email and password formats acceptable" + RESET)
        break

    student = database.find_student_by_email(email)

    if student is None or not student.login(password):
        print(TAB + RED + "Student does not exist" + RESET)
        return None

    return student


if __name__ == "__main__":
    from database import Database

    test_database = Database("students.data")
    student_menu(test_database)

