from dataclasses import dataclass

from core.errors import PermissionDeniedError


@dataclass
class UserSession:
    user_id: int
    _company_id: int | None = None
    _company_ids: list[int] | None = None

    def validate(self) -> None:
        if not isinstance(self.user_id, int):
            raise TypeError
        if not isinstance(self._company_id, int | None):
            raise TypeError
        if not isinstance(self._company_ids, list | None):
            raise TypeError
        
    @property
    def company_id(self) -> int:
        if not self._company_id:
            raise PermissionDeniedError(msg='user is not in the company')
        return self._company_id

    @company_id.setter
    def company_id(self, value):
        self._company_id = value

    @property
    def company_ids(self) -> list[int]:
        if not self._company_ids:
            raise PermissionDeniedError(msg='user is not in the company')
        return self._company_ids

    @company_ids.setter
    def company_ids(self, value):
        self._company_ids = value
