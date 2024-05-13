import strawberry

from .schemas import PaymentSchema
from .resolvers import create_payment_resolver


@strawberry.type
class PaymentMutations:
    create_payment: PaymentSchema = strawberry.mutation(
        resolver=create_payment_resolver,
    )
