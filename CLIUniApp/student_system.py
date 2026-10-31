
from student import Student
from validator import Validator


def student_menu(database):
    while True:
        choice = input("Student System (l/r/x): ").strip().lower()

        if choice == "l":
            student = login_account(database)

            if student is not None:
                print("Login successful")
                print("Enrolment System is not connected yet.")

        elif choice == "r":
            register_account(database)

        elif choice == "x":
            return

        else:
            print("Invalid option")


def register_account(database):
    print("Student Sign Up")

    while True:
        email = input("Email: ")
        password = input("Password: ")

        if not Validator.validate_credentials(email, password):
            print("Incorrect email or password format")
            continue

        print("email and password formats acceptable")
        break

    existing_student = database.find_student_by_email(email)

    if existing_student is not None:
        print(f"Student {existing_student.get_name()} already exists")
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
        print(f"Enrolling Student {name}")
    else:
        print("Student registration failed")


def login_account(database):
    print("Student Sign In")

    while True:
        email = input("Email: ")
        password = input("Password: ")

        if not Validator.validate_credentials(email, password):
            print("Incorrect email or password format")
            continue

        print("email and password formats acceptable")
        break

    student = database.find_student_by_email(email)

    if student is None or not student.login(password):
        print("Student does not exist")
        return None

    return student


if __name__ == "__main__":
    from database import Database

    test_database = Database("test_students.data")
    student_menu(test_database)

