from dataclasses import dataclass
from datetime import date


@dataclass
class GetContactsUsecaseDto:
    company_id: int
    first: int | None = None
    skip: int | None = None
    order_by: str | None = None


@dataclass
class GetContactUsecaseDto:
    id: int
    company_id: int | None = None


@dataclass
class CreateContactUsecaseDto:
    company_id: int
    created_by_id: int
    user_id: int | None
    first_name: str
    surname: str | None = None
    patronymic: str | None = None
    phone: str | None = None
    address: str | None = None
    birthday: date | None = None
    gender: str | None = None
    workplace: str | None = None
    job_title: str | None = None
    passport: str | None = None
    passport_issued_date: date | None = None
    passport_issued_place: str | None = None
