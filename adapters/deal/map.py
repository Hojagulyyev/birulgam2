from domain.deal.entities import Deal

from api.gql.deal.schemas import DealSchema


class DealMap:
    
    @classmethod
    def to_gql_schema(cls, deal: Deal):
        if not deal.id:
            raise TypeError
        if not deal.code_number:
            raise TypeError
        
        return DealSchema(
            id=deal.id,
            company_id=deal.company_id,
            store_id=deal.store_id,
            user_id=deal.user_id,
            seller_id=deal.seller_id,
            buyer_id=deal.buyer_id,

            store_code=deal.store_code,
            code_number=deal.code_number,
            total_amount=deal.total_amount,
            remaining_amount_due=deal.remaining_amount_due,
            type=deal.type,

            installments_total_amount=deal.installments_total_amount,
            installments=deal.installments,
            installment_amount=deal.installment_amount,
            installment_trifle=deal.installment_trifle,
            installment_expiration_date=deal.installment_expiration_date,
            created_at=deal.created_at,
            last_paid_at=deal.last_paid_at,
            closed_at=deal.closed_at,
            note=deal.note,
        )
