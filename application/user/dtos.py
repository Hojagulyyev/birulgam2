from dataclasses import dataclass

from application.error import InvalidError


@dataclass
class CreateUserUsecaseDto:
    username: str
    password: str
    company_id: int


@dataclass
class SignupUserUsecaseDto:
    username: str
    password: str
    password_confirm: str

    def validate(self):
        if self.password != self.password_confirm:
            raise InvalidError(
                loc=['body', 'password_confirm'], 
                msg='password mismatch',
            )
