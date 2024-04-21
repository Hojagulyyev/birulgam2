from dataclasses import dataclass

from domain.company.entities import Company


@dataclass
class User:
    company_id: int
    username: str
    password: str
    id: int | None = None

    company: Company | None = Company

    USERNAME_MIN_LENGTH = 3
    USERNAME_MAX_LENGTH = 20

    PASSWORD_MIN_LENGTH = 4
    PASSWORD_MAX_LENGTH = 26

    def __post_init__(self):
        if not isinstance(self.id, int | None):
            raise TypeError
        self._validate_username()
        self._validate_password()
        
    def _validate_username(self):
        if not isinstance(self.username, str):
            raise TypeError
        
        username_len = len(self.username)
        if (
            username_len < self.USERNAME_MIN_LENGTH
            or username_len > self.USERNAME_MAX_LENGTH
        ):
            raise ValueError(f'user username\'s length must be between {self.USERNAME_MIN_LENGTH} and {self.USERNAME_MAX_LENGTH}')
        
    def _validate_password(self):
        if not isinstance(self.password, str):
            raise TypeError
        
        password_len = len(self.password)
        if (
            password_len < self.PASSWORD_MIN_LENGTH
            or password_len > self.PASSWORD_MAX_LENGTH
        ):
            raise ValueError(f'user password\'s length must be between {self.PASSWORD_MIN_LENGTH} and {self.PASSWORD_MAX_LENGTH}')
