class AppError(Exception):

    def __init__(
        self,
        loc: list[str] | None = None,
        msg: str | None = None,
        type: str | None = None,
    ):
        if loc is None:
            self.loc = []

        self.loc = loc
        self.msg = msg
        self.type = type

    def serialize(self):
        return {
            'loc': self.loc,
            'msg': self.msg,
            'type': self.type,
        }


class InvalidError(AppError):
    def __init__(self, *args, **kwargs):
        super().__init__(type="invalid", *args, **kwargs)


class UniqueError(AppError):
    def __init__(self, *args, **kwargs):
        super().__init__(type="unique", *args, **kwargs)


class DoesNotExistError(AppError):
    def __init__(self, *args, **kwargs):
        super().__init__(type="does_not_exist", *args, **kwargs)


class PermissionDeniedError(AppError):
    def __init__(self, *args, **kwargs):
        super().__init__(type="permission_denied", *args, **kwargs)
