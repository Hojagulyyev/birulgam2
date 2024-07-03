from datetime import date

import strawberry

from ..company.schemas import CompanySchema
from ..user.schemas import UserSchema


@strawberry.type
class ContactSchema:
    # >>> RELATED
    company_id: int
    created_by_id: int
    user_id: int | None = None
    # >>> REQUIRED
    first_name: str
    # >>> OPTIONAL
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
    id: int | None = None
    # >>> MAP
    company: CompanySchema | None = None
    created_by: UserSchema | None = None
    user: UserSchema | None = None


@strawberry.type
class ContactsConnectionSchema:
    nodes: list[ContactSchema]
    count: int
    total: int
