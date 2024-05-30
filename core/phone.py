import re


def is_valid_phone(phone: str) -> bool:
    valid_phone_pattern = "^993\d{8}$" # type: ignore
    if re.match(valid_phone_pattern, phone):
        return True
    return False


def format_phone(phone: str):
    prefix = '993'
    if phone.startswith(prefix):
        return phone
    return prefix + phone
