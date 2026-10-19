import json
from pathlib import Path
from student import Student


class Database:
    def __init__(self, file_name="students.data"):
        self._file_name = Path(file_name)
        self._students = []

        if not self._file_name.exists():
            with open(self._file_name, "w", encoding="utf-8") as file:
                json.dump([], file)
        self.load_from_file()

    def load_from_file(self):
        with open(self._file_name, "r", encoding="utf-8") as file:
            data = json.load(file)

        students = []

        for record in data:
            student = Student(
                record["id"],
                record["name"],
                record["email"],
                record["password"],
                []
            )
            students.append(student)

        self._students = students
        return self._students



    def save_to_file(self):
        data = []

        for student in self._students:

            # 1. convert the student's Subject objects to dictionaries
            subjects_data = []

            for subject in student.get_enrolment_list():
                subject_record = {
                    "subject_id": subject.get_subject_id(),
                    "mark": subject.get_mark(),
                    "grade": subject.get_grade()
                }
                subjects_data.append(subject_record)

            # 2. convert Student object to dictionary
            record = {
                "id": student.get_id(),
                "name": student.get_name(),
                "email": student.get_email(),
                "password": student.get_password(),
                "subjects": subjects_data
            }

            data.append(record)

        # 3. save all students data to JSON
        with open(self._file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    
    def add_student(self, student):
        for existing_student in self._students:
            if existing_student.get_id() == student.get_id():
                return False

            if existing_student.get_email() == student.get_email():
                return False

        self._students.append(student)
        self.save_to_file()
        return True
    
    def find_student(self, student_id):
        for student in self._students:
            if student.get_id() == student_id:
                return student

        return None

    def find_student_by_email(self, email):
        for student in self._students:
            if student.get_email() == email:
                return student

        return None
    
    def get_all_students(self):
        return self._students.copy()
    
    def update_student(self, student):
        for index, existing_student in enumerate(self._students):
            if existing_student.get_id() == student.get_id():
                self._students[index] = student
                self.save_to_file()
                return True

        return False


if __name__ == "__main__":
    db = Database("test_students.data")

    print("Before:", len(db.get_all_students()))

    db.save_to_file()

    db2 = Database("test_students.data")

    print("After:", len(db2.get_all_students()))






       
