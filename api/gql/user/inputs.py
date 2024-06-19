import strawberry


@strawberry.input
class SignupUserInput:
    username: str
    password: str
    password_confirm: str


@strawberry.input
class SigninUserInput:
    username: str
    password: str


@strawberry.input
class SigninByOtpUserInput:
    phone: str
    otp: str
