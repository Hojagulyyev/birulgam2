from domain.user.interfaces import IUserRepository
from domain.user.entities import User

from application.user.errors import UserNotFoundError

from asyncpg import Connection, Record


class UserPgRepository(IUserRepository):

    def __init__(self, conn: Connection):
        self._conn = conn

    async def get_by_username(self, username: str) -> User:
        stmt = (
            '''
            SELECT id, username, company_id FROM users
            WHERE
                username = $1
            '''
        )
        row: Record = await self._conn.fetchrow(stmt, username)
        if row is None:
            raise UserNotFoundError

        user = User(
            id=row[0],
            username=row[1],
            company_id=row[2],
            password="secret",
        )
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
            INSERT INTO users 
            (
                username,
                password,
                company_id
            ) VALUES (
                $1, $2, $3
            )
            RETURNING id
            '''
        )
        args = (
            user.username, 
            user.password, 
            user.company_id, 
        )
        inserted_id = await self._conn.fetchval(stmt, *args)
        user.id = inserted_id
        return user

    async def _update(self, user: User) -> User:
        stmt = (
            '''
            UPDATE users SET 
                username = $1,
                password = $2,
                company_id = $3
            WHERE id = $4
            '''
        )
        args = (
            user.username, 
            user.password, 
            user.company_id, 
            user.id,
        )
        await self._conn.execute(stmt, *args)
        return user
