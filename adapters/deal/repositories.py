from asyncpg import Connection
from asyncpg.exceptions import ForeignKeyViolationError

from core.errors import InvalidError
from core.counter import Counter
from domain.deal.interfaces import IDealRepository
from domain.deal.entities import Deal, DealsConnection

from adapters.core.repositories import PgRepository


class DealPgRepository(PgRepository, IDealRepository):

    class Meta:
        columns = (
            'id',
            'company_id',
            'store_id',
            'created_by_id',
            'seller_id',
            'buyer_id',
            'store_code',
            'code_number',
            'total_amount',
            'remaining_amount_due',
            'type',
            'installments_total_amount',
            'installments',
            'installment_amount',
            'installment_trifle',
            'installment_expiration_date',
            'created_at',
            'last_paid_at',
            'closed_at',
            'note',
        )
        constraints = (
            'deal_store_id_fkey',
        )
    

    def __init__(self, conn: Connection):
        self._conn = conn

    async def list(
        self,
        company_id: int | None = None,
        ids: list[int] | None = None,
        type: str | None = None,
        first: int | None = None,
        skip: int | None = None,
        order_by: str | None = None,
    ) -> DealsConnection:
        stmt = (
            f'''
            SELECT
                {super().columns()},
                COUNT(*) OVER() AS total
            FROM deal
            WHERE 
                1 = 1
            '''
        )
        args = []

        if company_id:
            args.append(company_id)
            stmt += f'AND company_id = ${len(args)}'

        if type:
            args.append(type)
            stmt += f'AND type = ${len(args)}'

        if ids:
            param_position = len(args)+1
            args += ids
            ids_placeholder = ', '.join([f'${i+param_position}' for i in range(len(ids))])
            stmt += f'AND id IN ({ids_placeholder})'

        stmt, args = super().order_by(order_by, stmt, args)
        stmt, args = super().limit(first, stmt, args)
        stmt, args = super().offset(skip, stmt, args)

        rows = await self._conn.fetch(stmt, *args)
        with Counter() as c:
            deals: list[Deal] = [
                Deal(
                    id=row[c.start()],
                    company_id=row[c.auto()],
                    store_id=row[c.auto()],
                    created_by_id=row[c.auto()],
                    seller_id=row[c.auto()],
                    buyer_id=row[c.auto()],
                    store_code=row[c.auto()],
                    code_number=row[c.auto()],
                    total_amount=row[c.auto()],
                    remaining_amount_due=row[c.auto()],
                    type=row[c.auto()],
                    installments_total_amount=row[c.auto()],
                    installments=row[c.auto()],
                    installment_amount=row[c.auto()],
                    installment_trifle=row[c.auto()],
                    installment_expiration_date=row[c.auto()],
                    created_at=row[c.auto()],
                    last_paid_at=row[c.auto()],
                    closed_at=row[c.auto()],
                    note=row[c.auto()],
                )
                for row in rows
            ]
            total = rows[0][c.auto()] if rows else 0
        
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
            deal = await self._increment_code_number_by_store_id(deal)
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
                created_by_id,
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
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10,
                $11, $12, $13, $14, $15, $16, $17, $18, $19
            )
            RETURNING
                id, 
                code_number
            '''
        )
        args = (
                deal.company_id,
                deal.store_id,
                deal.created_by_id,
                deal.seller_id,
                deal.buyer_id,
                deal.store_code,
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
        )
        try:
            row = await self._conn.fetchrow(stmt, *args)
            if not row:
                raise ValueError
        except ForeignKeyViolationError as e:
            if self.Meta.constraints[0] in str(e):
                raise InvalidError(loc=['deal', 'store_id'])
            raise e

        deal.id = row[0]
        deal.code_number = row[1]
        return deal

    async def _update(self, deal: Deal) -> Deal:
        with Counter(1) as c:
            stmt = (
                f'''
                UPDATE deal SET 
                    company_id = ${c.auto()},
                    store_id = ${c.auto()},
                    created_by_id = ${c.auto()},
                    seller_id = ${c.auto()},
                    buyer_id = ${c.auto()},
                    code_number = ${c.auto()},
                    total_amount = ${c.auto()},
                    remaining_amount_due = ${c.auto()},
                    type = ${c.auto()},
                    installments_total_amount = ${c.auto()},
                    installments = ${c.auto()},
                    installment_amount = ${c.auto()},
                    installment_trifle = ${c.auto()},
                    installment_expiration_date = ${c.auto()},
                    created_at = ${c.auto()},
                    last_paid_at = ${c.auto()},
                    closed_at = ${c.auto()},
                    note = ${c.auto()}
                WHERE id = ${c.auto()}
                '''
            )
        args = (
            deal.company_id,
            deal.store_id,
            deal.created_by_id,
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

    async def _increment_code_number_by_store_id(self, deal: Deal) -> Deal:
        '''
        This function increments the deal code number by store.

        Use with caution due to (potential 
        for errors due to not clean query).
        '''
        stmt = (
            f'''
            UPDATE store SET
                next_{deal.type}_id = next_{deal.type}_id + 1
            WHERE id = $1
            RETURNING
                next_{deal.type}_id
            '''
        )
        new_code_number = await self._conn.fetchval(stmt, deal.store_id)
        if not new_code_number:
            raise ValueError

        deal.code_number = new_code_number - 1
        return deal
