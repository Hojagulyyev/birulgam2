from asyncpg import Connection
from asyncpg.exceptions import UniqueViolationError

from core.errors import (
    UniqueError,
)
from core.counter import Counter
from domain.store.interfaces import IStoreRepository
from domain.store.entities import Store


class StorePgRepository(IStoreRepository):

    class Constraints:
        uk_name = 'store__uk__company_id__name'
        uk_code = 'store__uk__company_id__code'

    columns = '''
        id,
        company_id,
        name,
        code
    '''

    def __init__(self, conn: Connection):
        self._conn = conn

    async def get_by_id(self, company_id: int | None, id: int) -> Store | None:
        stmt = (
            '''
            SELECT
            '''
            + self.columns + 
            '''
            FROM store
            WHERE
                id = $1
            '''
        )

        args = [id, ]

        if company_id:
            args.append(company_id)
            stmt += f'AND company_id = ${len(args)}'

        row = await self._conn.fetchrow(stmt, *args)
        if row is None:
            return None

        with Counter() as c:
            store = Store(
                id=row[c.auto()],
                company_id=row[c.auto()],
                name=row[c.auto()],
                code=row[c.auto()],
            )
        return store
        
    async def save(self, store: Store) -> Store:
        if not store.id:
            store = await self._insert(store)
        else:
            store = await self._update(store)
        return store
    
    async def _insert(self, store: Store) -> Store:
        stmt = (
            '''
            INSERT INTO store
            (
                company_id,
                name,
                code
            ) VALUES (
                $1, $2, $3
            )
            RETURNING id
            '''
        )
        args = (
            store.company_id,
            store.name,
            store.code,
        )
        try:
            store_id = await self._conn.fetchval(stmt, *args)
            if not store_id:
                raise ValueError
        except UniqueViolationError as e:
            if self.Constraints.uk_name in str(e):
                raise UniqueError(loc=['store', 'name'])
            if self.Constraints.uk_code in str(e):
                raise UniqueError(loc=['store', 'code'])
            raise e

        store.id = store_id
        return store

    async def _update(self, store: Store) -> Store:
        with Counter(1) as c:
            stmt = (
                f'''
                UPDATE store SET 
                    company_id = ${c.auto()},
                    name = ${c.auto()},
                    code = ${c.auto()}
                WHERE id = ${c.auto()}
                '''
            )
        args = (
            store.company_id,
            store.name,
            store.code,
            store.id,
        )
        await self._conn.execute(stmt, *args)
        return store
