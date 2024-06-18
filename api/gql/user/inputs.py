import strawberry


@strawberry.input
class SignupUserInput:
    username: str
    password: str
    password_confirm: str
