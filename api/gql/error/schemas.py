import strawberry


@strawberry.type
class ErrorSchema:
    loc: list[str] | None = None
    msg: str | None = None
    type_: str | None = None

    def __init__(self, loc=None, msg=None, type=None):
        self.loc = loc
        self.msg = msg
        self.type_ = type