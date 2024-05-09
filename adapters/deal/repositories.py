from asyncpg import Connection

from domain.deal.interfaces import IDealRepository
from domain.deal.entities import Deal


class DealPgRepository(IDealRepository):

    def __init__(self, conn: Connection):
        self._conn = conn
        
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
        except Exception as e:
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
