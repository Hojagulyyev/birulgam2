from domain.contact.entities import Contact

from api.gql.contact.schemas import ContactSchema


class ContactMap:
    
    @classmethod
    def to_gql_schema(cls, contact: Contact):
        if contact.id is None:
            raise TypeError
        
        return ContactSchema(
            id=contact.id,
            company_id=contact.company_id,
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
        )
