import strawberry


@strawberry.type
class SendOtpResponseSchema:
    phone: str
