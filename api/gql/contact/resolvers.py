from strawberry.types import Info

from application.contact.usecases import (
    CreateContactUsecase,
) 
from application.contact.dtos import (
    CreateContactUsecaseDto,
)
from adapters.contact.map import ContactMap
from adapters.contact.repositories import ContactPgRepository

from .schemas import ContactSchema
from .inputs import CreateContactInput


async def create_contact_resolver(
    info: Info,
    input: CreateContactInput,
) -> ContactSchema:
    async with info.context["pgpool"].acquire() as conn:
        contact_repo = ContactPgRepository(conn=conn)
        create_contact_usecase = CreateContactUsecase(
            contact_repo=contact_repo,
        )
        contact = await create_contact_usecase.execute(
            CreateContactUsecaseDto(
                company_id=input.company_id,
                first_name=input.first_name,
                surname=input.surname,
                patronymic=input.patronymic,
                phone=input.phone,
                address=input.address,
                birthday=input.birthday,
                gender=input.gender,
                workplace=input.workplace,
                job_title=input.job_title,
                passport=input.passport,
                passport_issued_date=input.passport_issued_date,
                passport_issued_place=input.passport_issued_place,
            ),
        )
    response = ContactMap.to_gql_schema(contact)
    return response
