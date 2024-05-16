from asyncpg import Connection
from asyncpg.exceptions import ForeignKeyViolationError

from domain.deal.interfaces import IDealRepository
from domain.deal.entities import Deal, DealPage

from application.errors import InvalidError


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
        total_amount,
        remaining_amount_due,
        type,
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
    ) -> DealPage:
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

        rows = await self._conn.fetch(stmt, *args)
        
        deals: list[Deal] = [
            Deal(
                id=row[0],
                company_id=row[1],
                store_id=row[2],
                user_id=row[3],
                seller_id=row[4],
                buyer_id=row[5],
                total_amount=row[6],
                remaining_amount_due=row[7],
                type=row[8],
                installments=row[9],
                installment_amount=row[10],
                installment_trifle=row[11],
                installment_expiration_date=row[12],
                created_at=row[13],
                last_paid_at=row[14],
                closed_at=row[15],
                note=row[16],
            )
            for row in rows
        ]
        total = rows[0][17] if rows else 0
        
        deal_page = DealPage(
            deals=deals,
            total=total,
        )
        return deal_page
    
    async def get_by_id(
        self, 
        id: int, 
        company_id: int | None = None,
    ) -> Deal | None:
        deal_page = await self.list(
            ids=[id],
            company_id=company_id,
        )
        if deal_page.total == 0:
            return None
        
        return deal_page.deals[0]
        
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
                total_amount,
                remaining_amount_due,
                type,
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
                $11, $12, $13, $14, $15, $16
            )
            RETURNING id
            '''
        )
        args = (
                deal.company_id,
                deal.store_id,
                deal.user_id,
                deal.seller_id,
                deal.buyer_id,
                deal.total_amount,
                deal.remaining_amount_due,
                deal.type,
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
            inserted_id = await self._conn.fetchval(stmt, *args)
        except ForeignKeyViolationError as e:
            if self.Constraints.fk_store_id in str(e):
                raise InvalidError(loc=['deal', 'store_id'])
            raise e

        deal.id = inserted_id
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
                total_amount = $6,
                remaining_amount_due = $7,
                type = $8,
                installments = $9,
                installment_amount = $10,
                installment_trifle = $11,
                installment_expiration_date = $12,
                created_at = $13,
                last_paid_at = $14,
                closed_at = $15,
                note = $16
            WHERE id = $17
            '''
        )
        args = (
            deal.company_id,
            deal.store_id,
            deal.user_id,
            deal.seller_id,
            deal.buyer_id,
            deal.total_amount,
            deal.remaining_amount_due,
            deal.type,
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
