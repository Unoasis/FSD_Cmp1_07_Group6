import re
import random


class Validator:
    @staticmethod
    def validate_email(email):
        pattern = r"^[a-zA-Z]+\.[a-zA-Z]+@university\.com$"
        if re.match(pattern, email):
            return True
        else:
            return False

    @staticmethod
    def validate_password(password):
        pattern = r"^[A-Z][a-zA-Z]{5,}\d{3,}$"
        if re.match(pattern, password):
            return True
        else:
            return False

    @staticmethod
    def validate_credentials(email, password):
        email_ok = Validator.validate_email(email)
        password_ok = Validator.validate_password(password)
        return email_ok and password_ok

    @staticmethod
    def generate_ID(existing_ids):
        while True:
            number = random.randint(1, 999999)
            new_id = str(number).zfill(6)
            if new_id not in existing_ids:
                return new_id


if __name__ == "__main__":
    existing = ["000001", "000002"]
    planned = [1, 2, 5]
    original_randint = random.randint

    def fake_randint(a, b):
        return planned.pop(0)

    random.randint = fake_randint
    new_id = Validator.generate_ID(existing)
    random.randint = original_randint

    print(new_id)
    print(new_id == "000005")
    print(len(planned) == 0)



