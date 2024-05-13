import strawberry


@strawberry.type
class ErrorSchema:
    loc: list[str] | None
    msg: str | None
    type_: str | None

    def __init__(self, loc, msg, type):
        self.loc = loc
        self.msg = msg
        self.type_ = type