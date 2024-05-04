class ContactNotFoundError(Exception):
    def __init__(self):
        super().__init__(f"contact not found")


class ContactPhoneMustBeUniqueError(Exception):
    def __init__(self):
        super().__init__(f"contact phone must be unique")
