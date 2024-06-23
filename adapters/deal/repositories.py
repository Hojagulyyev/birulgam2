from asyncpg import Connection
from asyncpg.exceptions import ForeignKeyViolationError

from core.errors import InvalidError
from core.pagination import MAX_LIMIT
from domain.deal.interfaces import IDealRepository
from domain.deal.entities import Deal, DealsConnection


class DealPgRepository(IDealRepository):

    class Constraints:
        fk_store_id = 'deal_store_id_fkey'

    columns = '''
        id,
        company_id,
        store_id,
        user_id,
        seller_id,
        buyer_id,
        store_code,
        code_number,
        total_amount,
        remaining_amount_due,
        type,
        installments_total_amount,
        installments,
        installment_amount,
        installment_trifle,
        installment_expiration_date,
        created_at,
        last_paid_at,
        closed_at,
        note
    '''

    def __init__(self, conn: Connection):
        self._conn = conn

    async def list(
        self,
        ids: list[int] | None = None,
        company_id: int | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> DealsConnection:
        stmt = (
            '''
            SELECT
            '''
            + self.columns + 
            '''
                ,
                COUNT(*) OVER() AS total
            FROM deal
            WHERE 
                1 = 1
            '''
        )
        args = []

        if ids:
            args += ids
            ids_placeholder = ', '.join([f'${i+1}' for i in range(len(ids))])
            stmt += f'AND id IN ({ids_placeholder})'

        if company_id:
            args.append(company_id)
            stmt += f'AND company_id = ${len(args)}'

        if not limit or limit <= 0:
            limit = MAX_LIMIT
        args.append(limit)
        stmt += f'LIMIT ${len(args)}'

        if not offset or offset < 0:
            offset = 0
        args.append(offset)
        stmt += f'OFFSET ${len(args)}'

        rows = await self._conn.fetch(stmt, *args)
        
        deals: list[Deal] = [
            Deal(
                id=row[0],
                company_id=row[1],
                store_id=row[2],
                user_id=row[3],
                seller_id=row[4],
                buyer_id=row[5],
                store_code=row[6],
                code_number=row[7],
                total_amount=row[8],
                remaining_amount_due=row[9],
                type=row[10],
                installments_total_amount=row[11],
                installments=row[12],
                installment_amount=row[13],
                installment_trifle=row[14],
                installment_expiration_date=row[15],
                created_at=row[16],
                last_paid_at=row[17],
                closed_at=row[18],
                note=row[19],
            )
            for row in rows
        ]
        total = rows[0][20] if rows else 0
        
        deals_connection = DealsConnection(
            deals=deals,
            count=len(deals),
            total=total,
        )
        return deals_connection
    
    async def get_by_id(
        self, 
        id: int, 
        company_id: int | None = None,
    ) -> Deal | None:
        deals_connection = await self.list(
            ids=[id],
            company_id=company_id,
        )
        if deals_connection.total == 0:
            return None
        
        return deals_connection.deals[0]
        
    async def save(self, deal: Deal) -> Deal:
        if not deal.id:
            deal = await self._insert(deal)
        else:
            deal = await self._update(deal)
        return deal
    
    async def _insert(self, deal: Deal) -> Deal:
        stmt = (
            '''
            INSERT INTO deal
            (
                company_id,
                store_id,
                user_id,
                seller_id,
                buyer_id,
                store_code,
                total_amount,
                remaining_amount_due,
                type,
                installments_total_amount,
                installments,
                installment_amount,
                installment_trifle,
                installment_expiration_date,
                created_at,
                last_paid_at,
                closed_at,
                note
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10,
                $11, $12, $13, $14, $15, $16, $17, $18
            )
            RETURNING
                id, 
                code_number
            '''
        )
        args = (
                deal.company_id,
                deal.store_id,
                deal.user_id,
                deal.seller_id,
                deal.buyer_id,
                deal.store_code,
                deal.total_amount,
                deal.remaining_amount_due,
                deal.type,
                deal.installments_total_amount,
                deal.installments,
                deal.installment_amount,
                deal.installment_trifle,
                deal.installment_expiration_date,
                deal.created_at,
                deal.last_paid_at,
                deal.closed_at,
                deal.note,
        )
        try:
            row = await self._conn.fetchrow(stmt, *args)
            if not row:
                raise ValueError
        except ForeignKeyViolationError as e:
            if self.Constraints.fk_store_id in str(e):
                raise InvalidError(loc=['deal', 'store_id'])
            raise e

        deal.id = row[0]
        deal.code_number = row[1]
        return deal

    async def _update(self, deal: Deal) -> Deal:
        stmt = (
            '''
            UPDATE deal SET 
                company_id = $1,
                store_id = $2,
                user_id = $3,
                seller_id = $4,
                buyer_id = $5,
                code_number = $6,
                total_amount = $7,
                remaining_amount_due = $8,
                type = $9,
                installments_total_amount = $10,
                installments = $11,
                installment_amount = $12,
                installment_trifle = $13,
                installment_expiration_date = $14,
                created_at = $15,
                last_paid_at = $16,
                closed_at = $17,
                note = $18
            WHERE id = $19
            '''
        )
        args = (
            deal.company_id,
            deal.store_id,
            deal.user_id,
            deal.seller_id,
            deal.buyer_id,
            deal.code_number,
            deal.total_amount,
            deal.remaining_amount_due,
            deal.type,
            deal.installments_total_amount,
            deal.installments,
            deal.installment_amount,
            deal.installment_trifle,
            deal.installment_expiration_date,
            deal.created_at,
            deal.last_paid_at,
            deal.closed_at,
            deal.note,
            deal.id,
        )
        await self._conn.execute(stmt, *args)
        return deal
