from asyncpg import Connection
from asyncpg.exceptions import UniqueViolationError

from domain.store.interfaces import IStoreRepository
from domain.store.entities import Store

from application.store.errors import (
    StoreNameMustBeUniqueError,
    StoreCodeMustBeUniqueError
)


class StorePgRepository(IStoreRepository):

    def __init__(self, conn: Connection):
        self._conn = conn
        
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
            inserted_id = await self._conn.fetchval(stmt, *args)
        except UniqueViolationError as e:
            if "store__uk__company_id__name" in str(e):
                raise StoreNameMustBeUniqueError
            if "store__uk__company_id__code" in str(e):
                raise StoreCodeMustBeUniqueError
            raise e

        store.id = inserted_id
        return store

    async def _update(self, store: Store) -> Store:
        stmt = (
            '''
            UPDATE store SET 
                company_id = $1,
                name = $2,
                code = $3
            WHERE id = $4
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
