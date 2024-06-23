from datetime import date

import strawberry

from ..company.schemas import CompanySchema
 
 
@strawberry.type
class ContactSchema:
    company_id: int
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
    id: int | None = None

    company: CompanySchema | None = None


@strawberry.type
class ContactsConnectionSchema:
    contacts: list[ContactSchema]
    count: int
    total: int
