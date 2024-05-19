from dataclasses import dataclass

from application.errors import InvalidError


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
                loc=['body', 'password_confirm'], 
                msg='password mismatch',
            )
