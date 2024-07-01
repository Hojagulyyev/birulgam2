from domain.payment.entities import Payment

from api.gql.payment.schemas import (
    PaymentSchema,
    PaymentTypeSchema,
    PaymentMethodSchema,
)
from api.gql.deal.schemas import DealTypeSchema
from adapters.deal.map import DealMap


class PaymentMap:
    
    @classmethod
    def to_gql_schema(cls, payment: Payment):
        return PaymentSchema(
            id=payment.id,
            company_id=payment.company_id,
            store_id=payment.store_id,
            user_id=payment.user_id,
            deal_id=payment.deal_id,
            sender_id=payment.sender_id,
            receiver_id=payment.receiver_id,

            amount=payment.amount,
            type=PaymentTypeSchema(payment.type),
            method=PaymentMethodSchema(payment.method),
            category=DealTypeSchema(payment.category),

            created_at=payment.created_at,

            deal=payment.deal and DealMap.to_gql_schema(payment.deal),
        )
