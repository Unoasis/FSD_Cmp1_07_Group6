import random


class Subject:
    MIN_ID = 1
    MAX_ID = 999
    MIN_MARK = 25
    MAX_MARK = 100

    def __init__(self, existing_ids):
        self._subject_id = self.generate_subject_ID(existing_ids)
        self._mark = self.generate_mark()
        self._grade = self.calculate_grade()

    def generate_subject_ID(self, existing_ids):
        new_id = self.format_id(random.randint(Subject.MIN_ID, Subject.MAX_ID))
        while new_id in existing_ids:
            new_id = self.format_id(random.randint(Subject.MIN_ID, Subject.MAX_ID))
        return new_id

    def format_id(self, number):
        if number < 10:
            return "00" + str(number)
        elif number < 100:
            return "0" + str(number)
        else:
            return str(number)

    def generate_mark(self):
        return random.randint(Subject.MIN_MARK, Subject.MAX_MARK)

    def calculate_grade(self):
        return Subject.grade_from_mark(self._mark)

    @staticmethod
    def grade_from_mark(mark):
        if mark < 50:
            return "Z"
        elif mark < 65:
            return "P"
        elif mark < 75:
            return "C"
        elif mark < 85:
            return "D"
        else:
            return "HD"

    def get_subject_id(self):
        return self._subject_id

    def get_mark(self):
        return self._mark

    def get_grade(self):
        return self._grade

    def __str__(self):
        return f"[ Subject::{self._subject_id} -- mark = {self._mark} -- grade = {self._grade:>3} ]"


if __name__ == "__main__":
    ids = []
    for i in range(4):
        subject = Subject(ids)
        ids.append(subject.get_subject_id())
        print(subject)

    print(Subject.grade_from_mark(49) == "Z")
    print(Subject.grade_from_mark(50) == "P")
    print(Subject.grade_from_mark(65) == "C")
    print(Subject.grade_from_mark(75) == "D")
    print(Subject.grade_from_mark(85) == "HD")
