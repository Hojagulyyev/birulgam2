import strawberry

from ..error.schemas import ErrorSchema
from .schemas import PaymentSchema
from .resolvers import (
    create_payment_resolver,
    create_payment_response,
)


@strawberry.type
class PaymentMutations:
    create_payment: create_payment_response = strawberry.mutation(
        resolver=create_payment_resolver,
    )
