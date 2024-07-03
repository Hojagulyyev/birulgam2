from domain.contact.entities import Contact

from adapters.user.map import UserMap
from api.gql.contact.schemas import ContactSchema


class ContactMap:
    
    @classmethod
    def to_gql_schema(cls, contact: Contact):
        if contact.id is None:
            raise TypeError
        
        contact_schema = ContactSchema(
            id=contact.id,
            company_id=contact.company_id,
            created_by_id=contact.created_by_id,
            user_id=contact.user_id,
            first_name=contact.first_name,
            surname=contact.surname,
            patronymic=contact.patronymic,
            phone=contact.phone,
            address=contact.address,
            birthday=contact.birthday,
            gender=contact.gender,
            workplace=contact.workplace,
            job_title=contact.job_title,
            passport=contact.passport,
            passport_issued_date=contact.passport_issued_date,
            passport_issued_place=contact.passport_issued_place,
            created_by=contact.created_by and UserMap.to_gql_schema(contact.created_by),
            user=contact.user and UserMap.to_gql_schema(contact.user),
        )
        return contact_schema
