from person import Person
from validator import Validator
from subject import Subject

class Student(Person):
    MAX_SUBJECTS = 4
    def __init__(self, student_id, name, email, password, enrolment_list=None):
        Person.__init__(self, name, email, password)
        self._id = student_id
        if enrolment_list is None:
            self._enrolment_list = []
        else:
            self._enrolment_list = enrolment_list
        self._average_mark = 0.0
        self.calculate_average_mark()

    def get_id(self):
        return self._id

    def get_enrolment_list(self):
        return self._enrolment_list

    def login(self, password):
        return password == self.get_password()

    def check_subject_limit(self):
        return len(self._enrolment_list) >= Student.MAX_SUBJECTS

    def enrol_subject(self):
        if self.check_subject_limit():
            return None
        existing_ids = []
        for subject in self._enrolment_list:
            existing_ids.append(subject.get_subject_id())
        new_subject = Subject(existing_ids)
        self.add_subject(new_subject)
        return new_subject

    def add_subject(self, subject):
        self._enrolment_list.append(subject)
        self.calculate_average_mark()

    def remove_subject(self, subject_id):
        for subject in self._enrolment_list:
            if subject.get_subject_id() == subject_id:
                self._enrolment_list.remove(subject)
                self.calculate_average_mark()
                return True
        return False

    def view_enrolment(self):
        return self._enrolment_list

    def update_password(self, new_password):
        if Validator.validate_password(new_password):
            self.set_password(new_password)
            return True
        return False

    def calculate_average_mark(self):
        if len(self._enrolment_list) == 0:
            self._average_mark = 0.0
        else:
            total = 0
            for subject in self._enrolment_list:
                total += subject.get_mark()
            self._average_mark = total / len(self._enrolment_list)
        return self._average_mark

    def get_average_mark(self):
        return self._average_mark

if __name__ == "__main__":
    s = Student("000001", "Alen Jones", "alen.jones@university.com", "Helloworld123")
    print(s.get_id())
    print(s.get_name())
    print(s.get_email())
    print(s.get_enrolment_list())
    print(s.login("Helloworld123"))
    print(s.login("wrong"))
    print(s.get_average_mark())