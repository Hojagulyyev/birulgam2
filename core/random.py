import random
import string


def generate_random_string(length: int = 6):
    random_generated_string = "".join(
        random.sample(string.ascii_lowercase, length)
    )
    return random_generated_string


def generate_otp() -> str:
    otp = random.randint(100000, 999999)
    return str(otp)
