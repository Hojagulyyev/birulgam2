from domain.contact.entities import Contact
from domain.contact.interfaces import (
    IContactRepository, 
)

from .dtos import (
    CreateContactUsecaseDto,
) 


class CreateContactUsecase:

    def __init__(
        self, 
        contact_repo: IContactRepository,
    ):
        self.contact_repo = contact_repo

    async def execute(self, dto: CreateContactUsecaseDto) -> Contact:
        contact = Contact(
            company_id=dto.company_id,
            first_name=dto.first_name,
            surname=dto.surname,
            patronymic=dto.patronymic,
            phone=dto.phone,
            address=dto.address,
            birthday=dto.birthday,
            gender=dto.gender,
            workplace=dto.workplace,
            job_title=dto.job_title,
            passport=dto.passport,
            passport_issued_date=dto.passport_issued_date,
            passport_issued_place=dto.passport_issued_place,
        )
        created_contact = await self.contact_repo.save(contact)
        return created_contact
    