from asyncpg import Connection
from asyncpg.exceptions import UniqueViolationError

from core.errors import (
    UniqueError,
)
from domain.contact.interfaces import IContactRepository
from domain.contact.entities import Contact, ContactsConnection

from adapters.core.repositories import PgRepository


class ContactPgRepository(PgRepository, IContactRepository):

    class Constraints:
        uk_phone = 'contact__uk__company_id__phone'

    columns = '''
        id,
        company_id,
        first_name,
        surname,
        patronymic,
        phone,
        address,
        birthday,
        gender,
        workplace,
        job_title,
        passport,
        passport_issued_date,
        passport_issued_place
    '''

    def __init__(self, conn: Connection):
        self._conn = conn

    async def list(
        self, 
        company_id: int | None,
        first: int | None = None,
        skip: int | None = None,
        order_by: str | None = None,
    ) -> ContactsConnection:
        stmt = (
            '''
            SELECT
            '''
            + self.columns + 
            '''
                ,
                COUNT(*) OVER() AS total
            FROM contact
            WHERE 
                1 = 1
            '''
        )
        args = []

        if company_id:
            args.append(company_id)
            stmt += f'AND company_id = ${len(args)}'

        stmt, args = super().order_by(order_by, stmt, args, self.columns)
        stmt, args = super().limit(first, stmt, args)
        stmt, args = super().offset(skip, stmt, args)

        rows = await self._conn.fetch(stmt, *args)
        contacts: list[Contact] = [
            Contact(
                id=row[0],
                company_id=row[1],
                first_name=row[2],
                surname=row[3],
                patronymic=row[4],
                phone=row[5],
                address=row[6],
                birthday=row[7],
                gender=row[8],
                workplace=row[9],
                job_title=row[10],
                passport=row[11],
                passport_issued_date=row[12],
                passport_issued_place=row[13],
            )
            for row in rows
        ]
        total = rows[0][14] if rows else 0
        
        contacts_connection = ContactsConnection(
            contacts=contacts,
            count=len(contacts),
            total=total,
        )
        return contacts_connection
        
    async def save(self, contact: Contact) -> Contact:
        if not contact.id:
            contact = await self._insert(contact)
        else:
            contact = await self._update(contact)
        return contact
    
    async def _insert(self, contact: Contact) -> Contact:
        stmt = (
            '''
            INSERT INTO contact
            (
                company_id,
                first_name,
                surname,
                patronymic,
                phone,
                address,
                birthday,
                gender,
                workplace,
                job_title,
                passport,
                passport_issued_date,
                passport_issued_place
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, 
                $8, $9, $10, $11, $12, $13
            )
            RETURNING id
            '''
        )
        args = (
            contact.company_id,
            contact.first_name,
            contact.surname,
            contact.patronymic,
            contact.phone,
            contact.address,
            contact.birthday,
            contact.gender,
            contact.workplace,
            contact.job_title,
            contact.passport,
            contact.passport_issued_date,
            contact.passport_issued_place,
        )
        try:
            contact_id = await self._conn.fetchval(stmt, *args)
            if not contact_id:
                raise ValueError
        except UniqueViolationError as e:
            if self.Constraints.uk_phone in str(e):
                raise UniqueError(loc=['contact', 'phone'])
            raise e

        contact.id = contact_id
        return contact

    async def _update(self, contact: Contact) -> Contact:
        stmt = (
            '''
            UPDATE contact SET 
                company_id = $1,
                first_name = $2,
                surname = $3,
                patronymic = $4,
                phone = $5,
                address = $6,
                birthday = $7,
                gender = $8,
                workplace = $9,
                job_title = $10,
                passport = $11,
                passport_issued_date = $12,
                passport_issued_place = $13
            WHERE id = $14
            '''
        )
        args = (
            contact.company_id,
            contact.first_name,
            contact.surname,
            contact.patronymic,
            contact.phone,
            contact.address,
            contact.birthday,
            contact.gender,
            contact.workplace,
            contact.job_title,
            contact.passport,
            contact.passport_issued_date,
            contact.passport_issued_place,
            contact.id,
        )
        await self._conn.execute(stmt, *args)
        return contact
