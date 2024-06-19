import strawberry


@strawberry.input
class SendOtpInput:
    phone: str
