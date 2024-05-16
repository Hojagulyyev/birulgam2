from asyncpg import Connection

from domain.payment.interfaces import IPaymentRepository
from domain.payment.entities import Payment, PaymentPage


class PaymentPgRepository(IPaymentRepository):

    class Constraints:
        pass

    columns = '''
        id,
        company_id,
        store_id,
        user_id,
        deal_id,
        sender_id,
        receiver_id,
        amount,
        type,
        method,
        category,
        created_at
    '''

    def __init__(self, conn: Connection):
        self._conn = conn

    async def list(
        self,
        ids: list[int] | None = None,
        company_id: int | None = None,
    ) -> PaymentPage:
        stmt = (
            '''
            SELECT
            '''
            + self.columns + 
            '''
                ,
                COUNT(*) OVER() AS total
            FROM payment
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
        
        payments: list[Payment] = [
            Payment(
                id=row[0],
                company_id=row[1],
                store_id=row[2],
                user_id=row[3],
                deal_id=row[4],
                sender_id=row[5],
                receiver_id=row[6],
                amount=row[7],
                type=row[8],
                method=row[9],
                category=row[10],
                created_at=row[11],
            )
            for row in rows
        ]
        total = rows[0][12] if rows else 0
        
        payment_page = PaymentPage(
            payments=payments,
            total=total,
        )
        return payment_page
    
    async def get_by_id(
        self, 
        id: int, 
        company_id: int | None = None,
    ) -> Payment | None:
        payment_page = await self.list(
            ids=[id],
            company_id=company_id,
        )
        if payment_page.total == 0:
            return None
        
        return payment_page.payments[0]
        
    async def save(self, payment: Payment) -> Payment:
        if not payment.id:
            payment = await self._insert(payment)
        else:
            payment = await self._update(payment)
        return payment
    
    async def _insert(self, payment: Payment) -> Payment:
        stmt = (
            '''
            INSERT INTO payment
            (
                company_id,
                store_id,
                user_id,
                deal_id,
                sender_id,
                receiver_id,
                amount,
                type,
                method,
                category,
                created_at
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10,
                $11
            )
            RETURNING id
            '''
        )
        args = (
            payment.company_id,
            payment.store_id,
            payment.user_id,
            payment.deal_id,
            payment.sender_id,
            payment.receiver_id,
            payment.amount,
            payment.type,
            payment.method,
            payment.category,
            payment.created_at,
        )
        try:
            inserted_id = await self._conn.fetchval(stmt, *args)
        except Exception as e:
            raise e

        payment.id = inserted_id
        return payment

    async def _update(self, payment: Payment) -> Payment:
        stmt = (
            '''
            UPDATE payment SET 
                company_id = $1,
                store_id = $2,
                user_id = $3,
                deal_id = $4,
                sender_id = $5,
                receiver_id = $6,
                amount = $7,
                type = $8,
                method = $9,
                category = $10,
                created_at = $11
            WHERE id = $12
            '''
        )
        args = (
            payment.company_id,
            payment.store_id,
            payment.user_id,
            payment.deal_id,
            payment.sender_id,
            payment.receiver_id,
            payment.amount,
            payment.type,
            payment.method,
            payment.category,
            payment.created_at,
            payment.id,
        )
        await self._conn.execute(stmt, *args)
        return payment
