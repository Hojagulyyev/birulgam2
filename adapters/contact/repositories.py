from asyncpg import Connection
from asyncpg.exceptions import UniqueViolationError

from core.errors import (
    UniqueError,
)
from core.counter import Counter
from domain.contact.interfaces import IContactRepository
from domain.contact.entities import Contact, ContactsConnection

from adapters.core.repositories import PgRepository


class ContactPgRepository(PgRepository, IContactRepository):

    class Meta:
        columns = (
            'id',
            'company_id',
            'created_by_id',
            'user_id',
            'first_name',
            'surname',
            'patronymic',
            'phone',
            'address',
            'birthday',
            'gender',
            'workplace',
            'job_title',
            'passport',
            'passport_issued_date',
            'passport_issued_place',
        )
        constraints = (
            'contact__uk__company_id__phone',
            'contact__uk__user_id__created_by_id',
        )

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
            f'''
            SELECT
                {super().columns()},
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

        stmt, args = super().order_by(order_by, stmt, args)
        stmt, args = super().limit(first, stmt, args)
        stmt, args = super().offset(skip, stmt, args)

        rows = await self._conn.fetch(stmt, *args)
        with Counter() as c:
            contacts: list[Contact] = [
                Contact(
                    id=row[c.start()],
                    company_id=row[c.auto()],
                    created_by_id=row[c.auto()],
                    user_id=row[c.auto()],
                    first_name=row[c.auto()],
                    surname=row[c.auto()],
                    patronymic=row[c.auto()],
                    phone=row[c.auto()],
                    address=row[c.auto()],
                    birthday=row[c.auto()],
                    gender=row[c.auto()],
                    workplace=row[c.auto()],
                    job_title=row[c.auto()],
                    passport=row[c.auto()],
                    passport_issued_date=row[c.auto()],
                    passport_issued_place=row[c.auto()],
                )
                for row in rows
            ]
            total = rows[0][c.auto()] if rows else 0
        
        contacts_connection = ContactsConnection(
            nodes=contacts,
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
                created_by_id,
                user_id,
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
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, 
                $11, $12, $13, $14, $15
            )
            RETURNING id
            '''
        )
        args = (
            contact.company_id,
            contact.created_by_id,
            contact.user_id,
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
            if self.Meta.constraints[0] in str(e):
                raise UniqueError(loc=['contact', 'phone'])
            if self.Meta.constraints[1] in str(e):
                raise UniqueError(
                    'the user must have one contact for himself',
                    loc=['contact', 'user_id'],
                )
            raise e

        contact.id = contact_id
        return contact

    async def _update(self, contact: Contact) -> Contact:
        with Counter() as c:
            stmt = (
                f'''
                UPDATE contact SET 
                    company_id = ${c.auto()},
                    created_by_id = ${c.auto()},
                    user_id = ${c.auto()},
                    first_name = ${c.auto()},
                    surname = ${c.auto()},
                    patronymic = ${c.auto()},
                    phone = ${c.auto()},
                    address = ${c.auto()},
                    birthday = ${c.auto()},
                    gender = ${c.auto()},
                    workplace = ${c.auto()},
                    job_title = ${c.auto()},
                    passport = ${c.auto()},
                    passport_issued_date = ${c.auto()},
                    passport_issued_place = ${c.auto()}
                WHERE id = ${c.auto()}
                '''
            )
        args = (
            contact.company_id,
            contact.created_by_id,
            contact.user_id,
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
