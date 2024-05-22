from strawberry.types import Info

from core.errors import Error
from domain.user_session.entities import UserSession

from application.contact.usecases import (
    CreateContactUsecase,
    GetContactsUsecase,
) 
from application.contact.dtos import (
    GetContactsUsecaseDto,
    CreateContactUsecaseDto,
)

from adapters.contact.map import ContactMap
from adapters.contact.repositories import ContactPgRepository

from ..error.schemas import ErrorSchema
from .schemas import ContactSchema, ContactPageSchema
from .inputs import (
    GetContactsInput,
    CreateContactInput,
)


async def get_contacts_resolver(
    info: Info,
    input: GetContactsInput,
) -> ContactPageSchema:
    async with info.context["pgpool"].acquire() as conn:
        contact_repo = ContactPgRepository(conn=conn)
        get_contacts_usecase = GetContactsUsecase(
            contact_repo=contact_repo,
        )
        contact_page = await get_contacts_usecase.execute(
            dto=GetContactsUsecaseDto(
                company_id=input.company_id,
            )
        )
    
    contact_schema_list = [
        ContactMap.to_gql_schema(contact)
        for contact in contact_page.contacts
    ]
    response = ContactPageSchema(
        contacts=contact_schema_list,
        total=contact_page.total,
    )
    return response


async def create_contact_resolver(
    info: Info,
    input: CreateContactInput,
) -> ContactSchema | ErrorSchema:
    user_session: UserSession = info.context["user_session"]
    try:
        async with info.context["pgpool"].acquire() as conn:
            contact_repo = ContactPgRepository(conn=conn)
            create_contact_usecase = CreateContactUsecase(
                contact_repo=contact_repo,
            )
            contact = await create_contact_usecase.execute(
                CreateContactUsecaseDto(
                    company_id=user_session.company_id,
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
    except Error as e:
        return ErrorSchema(**e.serialize())
    
    response = ContactMap.to_gql_schema(contact)
    return response
