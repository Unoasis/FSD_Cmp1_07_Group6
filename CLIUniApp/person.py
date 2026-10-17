class Person:
    def __init__(self, name, email, password):
        self._name = name
        self._email = email
        self._password = password

    def get_name(self):
        return self._name

    def get_email(self):
        return self._email

    def get_password(self):
        return self._password

    def set_password(self, new_password):
        self._password = new_password


if __name__ == "__main__":
    p = Person("Alen Jones", "alen.jones@university.com", "Helloworld123")
    print(p.get_name())
    print(p.get_email())
    print(p.get_password())
    p.set_password("Neworld123")
    print(p.get_password())
