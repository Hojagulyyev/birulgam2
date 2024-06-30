from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError

from core.errors import UniqueError
from core.counter import Counter
from domain.user.interfaces import IUserRepository
from domain.user.entities import User, UsersConnection
from domain.company.entities import Company


class UserPgRepository(IUserRepository):

    class Constraints:
        uk_username = 'user__uk__username'
        uk_phone = 'user__uk__phone'

    columns = '''
        id,
        username,
        password,
        phone
    '''

    def __init__(self, conn: Connection):
        self._conn = conn

    async def list(
        self, 
        ids: list[int] | None = None,
    ) -> UsersConnection:
        stmt = (
            '''
            SELECT
            '''
            + self.columns + 
            '''
                ,
                COUNT(*) OVER() AS total
            FROM user_
            WHERE
                1 = 1
            '''
        )
        args = []

        if ids:
            args += ids
            ids_placeholder = ', '.join([f'${i+1}' for i in range(len(ids))])
            stmt += f'AND id IN ({ids_placeholder})'

        rows = await self._conn.fetch(stmt, *args)

        with Counter() as c:
            users: list[User] = [
                User(
                    id=row[c.auto()],
                    username=row[c.auto()],
                    password=row[c.auto()],
                    phone=row[c.auto()],
                )
                for row in rows
            ]
            total = rows[0][c.auto()] if rows else 0

        users_connection = UsersConnection(
            users=users,
            total=total,
        )
        return users_connection
    
    # TODO: perf: use get by id stmt directly instead of using list()
    async def get_by_id(self, id: int) -> User | None:
        users_connection = await self.list(ids=[id])
        if users_connection.total == 0:
            return None
        return users_connection.users[0]

    async def get_by_username(self, username: str) -> User | None:
        stmt = (
            '''
            SELECT
            '''
            + self.columns + 
            '''
            FROM user_
            WHERE
                username = $1
            '''
        )
        row = await self._conn.fetchrow(stmt, username)
        if row is None:
            return None

        with Counter() as c:
            user = User(
                id=row[c.auto()],
                username=row[c.auto()],
                password=row[c.auto()],
                phone=row[c.auto()],
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
                user_company.user_id = $1
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
        user.companies = companies
        return user
        
    async def save(self, user: User) -> User:
        try:
            if not user.id:
                user = await self._insert(user)
            else:
                user = await self._update(user)

        except UniqueViolationError as e:
            if self.Constraints.uk_username in str(e):
                raise UniqueError(loc=['user', 'username'])
            if self.Constraints.uk_phone in str(e):
                raise UniqueError(loc=['user', 'phone'])
            raise e
        
        return user
    
    async def _insert(self, user: User) -> User:
        # >>> MAIN
        stmt = (
            '''
            INSERT INTO user_
            (
                username,
                password,
                phone
            ) VALUES (
                $1, $2, $3
            )
            RETURNING id
            '''
        )
        args = (
            user.username, 
            user.password,
            user.phone,
        )
        user_id = await self._conn.fetchval(stmt, *args)
        if not user_id:
            raise ValueError
        
        # >>> M2M: user.company_ids
        if user.company_ids:
            stmt = (
                f'''
                INSERT INTO user_company
                (
                    user_id,
                    company_id
                ) VALUES 
                {', '.join([
                    f'({user_id}, ${i+1})'
                    for i in range(len(user.company_ids))
                ])}
                '''
            )
            args = (company_id for company_id in user.company_ids)
            await self._conn.execute(stmt, *args)

        # >>> REPSONSE
        user.id = user_id
        return user

    async def _update(self, user: User) -> User:
        # >>> MAIN
        with Counter() as c:
            stmt = (
                f'''
                UPDATE user_ SET 
                    username = ${c.auto()},
                    password = ${c.auto()},
                    phone = ${c.auto()}
                WHERE id = ${c.auto()}
                '''
            )
        args = (
            user.username, 
            user.password, 
            user.phone,
            user.id,
        )
        await self._conn.execute(stmt, *args)
        
        # >>> M2M: user.company_ids
        if user.company_ids:
            stmt = (
                f'''
                DELETE FROM user_company
                WHERE
                    user_id = $1
                AND 
                    company_id IN ({
                        ', '.join([
                            f'${i+2}' 
                            for i in range(len(user.company_ids))
                        ])
                    })
                '''
            )
            args = (
                user.id,
                *(company_id for company_id in user.company_ids),
            )
            await self._conn.execute(stmt, *args)

            stmt = (
                f'''
                INSERT INTO user_company
                (
                    user_id,
                    company_id
                ) VALUES 
                {', '.join([
                    f'({user.id}, ${i+1})'
                    for i in range(len(user.company_ids))
                ])}
                '''
            )
            args = (company_id for company_id in user.company_ids)
            await self._conn.execute(stmt, *args)
        return user
