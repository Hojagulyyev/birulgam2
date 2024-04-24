class UserNotFoundError(Exception):
    def __init__(self):
        super().__init__(f"user not found")


class UsernameMustBeUniqueError(Exception):
    def __init__(self):
        super().__init__(f"username must be unique")