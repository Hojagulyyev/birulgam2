from datetime import date
from typing import Annotated

import strawberry


@strawberry.input
class CreateContactInput:
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
