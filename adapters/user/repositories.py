from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError

from domain.user.interfaces import IUserRepository
from domain.user.entities import User
from domain.company.entities import Company

from application.errors import UniqueError, DoesNotExistError


class UserPgRepository(IUserRepository):

    class Constraints:
        uk_username = 'user__uk__username'

    def __init__(self, conn: Connection):
        self._conn = conn

    async def get_by_username(self, username: str) -> User:
        stmt = (
            '''
            SELECT id, username, password FROM user_
            WHERE
                username = $1
            '''
        )
        row = await self._conn.fetchrow(stmt, username)
        if row is None:
            raise DoesNotExistError(loc=['user', 'username'])

        user = User(
            id=row[0],
            username=row[1],
            password=row[2],
            company_ids=[],
        )
        return user
    
    async def join_companies(self, user: User) -> User:
        stmt = (
            '''
            SELECT
                company.id,
                company.name
            FROM user_company
            LEFT JOIN company ON 
                company.id = user_company.company_id
            WHERE
                user_id = $1
            '''
        )
        rows = await self._conn.fetch(stmt, user.id)

        companies: list[Company] = [
            Company(
                id=row[0],
                name=row[1],
            )
            for row in rows
        ]
        user.companies =companies
        return user
        
    async def save(self, user: User) -> User:
        if not user.id:
            user = await self._insert(user)
        else:
            user = await self._update(user)
        return user
    
    async def _insert(self, user: User) -> User:
        stmt = (
            '''
            INSERT INTO user_
            (
                username,
                password
            ) VALUES (
                $1, $2
            )
            RETURNING id
            '''
        )
        args = (
            user.username, 
            user.password,
        )
        try:
            inserted_id = await self._conn.fetchval(stmt, *args)
        except UniqueViolationError as e:
            if self.Constraints.uk_username in str(e):
                raise UniqueError(loc=['user', 'username'])
            raise e

        user.id = inserted_id
        return user

    async def _update(self, user: User) -> User:
        stmt = (
            '''
            UPDATE user_ SET 
                username = $1,
                password = $2
            WHERE id = $3
            '''
        )
        args = (
            user.username, 
            user.password, 
            user.id,
        )
        await self._conn.execute(stmt, *args)
        return user
