class Error(Exception):

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


class InvalidError(Error):
    def __init__(self, *args, **kwargs):
        super().__init__(type="invalid", *args, **kwargs)


class UniqueError(Error):
    def __init__(self, *args, **kwargs):
        super().__init__(type="unique", *args, **kwargs)


class DoesNotExistError(Error):
    def __init__(self, *args, **kwargs):
        super().__init__(type="does_not_exist", *args, **kwargs)


class PermissionDeniedError(Error):
    def __init__(self, *args, **kwargs):
        super().__init__(type="permission_denied", *args, **kwargs)
