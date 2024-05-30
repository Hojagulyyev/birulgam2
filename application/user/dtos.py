from dataclasses import dataclass

from core.errors import InvalidError


@dataclass
class CreateUserUsecaseDto:
    username: str
    password: str
    company_ids: list[int]


@dataclass
class SignupUserUsecaseDto:
    username: str
    password: str
    password_confirm: str
    create_company: bool

    def validate(self):
        if self.password != self.password_confirm:
            raise InvalidError(
                loc=['input', 'password_confirm'], 
                msg='password mismatch',
            )


@dataclass
class SigninUserUsecaseDto:
    username: str
    password: str
