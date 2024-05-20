from asyncpg import Connection
from asyncpg.exceptions import UniqueViolationError

from domain.company.interfaces import ICompanyRepository
from domain.company.entities import Company

from application.errors import UniqueError


class CompanyPgRepository(ICompanyRepository):

    class Constraints:
        uk_name = 'company__uk__name'

    def __init__(self, conn: Connection):
        self._conn = conn
        
    async def save(self, company: Company) -> Company:
        if not company.id:
            company = await self._insert(company)
        else:
            company = await self._update(company)
        return company
    
    async def _insert(self, company: Company) -> Company:
        stmt = (
            '''
            INSERT INTO company 
            (
                name
            ) 
            VALUES (
                $1
            )
            RETURNING id
            '''
        )
        args = (company.name,)
        try:
            inserted_id = await self._conn.fetchval(stmt, *args)
            if not inserted_id:
                raise ValueError
        except UniqueViolationError as e:
            if self.Constraints.uk_name in str(e):
                raise UniqueError(loc=['company', 'name'])
            raise e
        
        company.id = inserted_id
        return company

    async def _update(self, company: Company) -> Company:
        stmt = (
            '''
            UPDATE company SET 
                name = $1 
            WHERE id = $2
            '''
        )
        args = (company.name, company.id)
        await self._conn.execute(stmt, *args)
        return company
