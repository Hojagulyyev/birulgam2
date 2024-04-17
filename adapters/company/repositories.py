from domain.company.interfaces import ICompanyRepository
from domain.company.entities import Company

from asyncpg import Connection


class CompanyPgRepository(ICompanyRepository):

    def __init__(self, conn: Connection):
        self._conn = conn
        
    async def save(self, company: Company) -> Company:
        if not company.id:
            stmt = await self._conn.prepare(
                '''
                INSERT INTO companies (name) VALUES (:name)
                '''
            )
            data = {'name': company.name}
        else:
            stmt = await self._conn.prepare(
                '''
                UPDATE companys SET name = :name WHERE id = :id
                '''
            )
            data = {'name': company.name, 'id': company.id}

        rows = await stmt.execute(data)
        
        if not company.id:
            company.id = rows[0]['id']

        return company
