from domain.company.interfaces import ICompanyRepository
from domain.company.entities import Company

from asyncpg import Connection


class CompanyPgRepository(ICompanyRepository):

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
            INSERT INTO companies 
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
        inserted_id = await self._conn.fetchval(stmt, *args)
        company.id = inserted_id
        return company

    async def _update(self, company: Company) -> Company:
        stmt = (
            '''
            UPDATE companies SET 
                name = $1 
            WHERE id = $2
            '''
        )
        args = (company.name, company.id)
        await self._conn.execute(stmt, *args)
        return company
