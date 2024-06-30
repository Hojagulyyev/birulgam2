from dataclasses import dataclass

from core.errors import InvalidError
from core.phone import is_valid_phone, format_phone


@dataclass
class CreateUserUsecaseDto:
    username: str
    password: str
    phone: str
    company_ids: list[int]


@dataclass
class SigninUserUsecaseDto:
    username: str
    password: str


@dataclass
class SignoutUserUsecaseDto:
    access_token: str
