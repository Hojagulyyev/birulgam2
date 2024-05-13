from domain.payment.entities import Payment

from api.gql.payment.schemas import PaymentSchema


class PaymentMap:
    
    @classmethod
    def to_gql_schema(cls, payment: Payment):
        if payment.id is None:
            raise TypeError
        
        return PaymentSchema(
            id=payment.id,
            company_id=payment.company_id,
            store_id=payment.store_id,
            user_id=payment.user_id,
            deal_id=payment.deal_id,
            sender_id=payment.sender_id,
            receiver_id=payment.receiver_id,

            amount=payment.amount,
            type=payment.type,
            method=payment.method,
            category=payment.category,

            created_at=payment.created_at,
        )
