from dataclasses import dataclass

from core.errors import PermissionDeniedError


@dataclass
class UserSession:
    _user_id: int
    _company_id: int
    _access_token: str

    def validate(self) -> None:
        if not isinstance(self._user_id, int):
            raise TypeError
        if not isinstance(self._company_id, int):
            raise TypeError
        if not isinstance(self._access_token, str):
            raise TypeError

    @property
    def user_id(self):
        if not self._user_id:
            raise PermissionDeniedError('user is not authenticated')
        return self._user_id
    
    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    def user_exists(self):
        return self._user_id != 0
    
    @property
    def access_token(self):
        if not self._access_token:
            raise PermissionDeniedError('user is not authenticated')
        return self._access_token
    
    @access_token.setter
    def access_token(self, value):
        self._access_token = value

    @property
    def company_id(self):
        if not self._company_id:
            raise PermissionDeniedError('user is not in the company')
        return self._company_id
    
    @company_id.setter
    def company_id(self, value):
        self._company_id = value

    def company_exists(self):
        return self._company_id != 0
