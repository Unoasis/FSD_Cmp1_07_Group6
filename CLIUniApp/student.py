from person import Person


class Student(Person):
    def __init__(self, student_id, name, email, password, enrolment_list=None):
        Person.__init__(self, name, email, password)
        self._id = student_id
        if enrolment_list is None:
            self._enrolment_list = []
        else:
            self._enrolment_list = enrolment_list

    def get_id(self):
        return self._id

    def get_enrolment_list(self):
        return self._enrolment_list

    def login(self, password):
        return password == self.get_password()


if __name__ == "__main__":
    s = Student("000001", "Alen Jones", "alen.jones@university.com", "Helloworld123")
    print(s.get_id())
    print(s.get_name())
    print(s.get_email())
    print(s.get_enrolment_list())
    print(s.login("Helloworld123"))
    print(s.login("wrong"))
