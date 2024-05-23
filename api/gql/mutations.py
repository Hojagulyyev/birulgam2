import strawberry

from .contact.resolvers import (
    create_contact_resolver,
    create_contact_response,
)
from .deal.resolvers import (
    create_deal_resolver,
    create_deal_response,
)
from .payment.resolvers import (
    create_payment_resolver,
    create_payment_response,
)


@strawberry.type
class Mutation:
    create_contact: create_contact_response = strawberry.mutation(
        resolver=create_contact_resolver)
    create_deal: create_deal_response = strawberry.mutation(
        resolver=create_deal_resolver)
    create_payment: create_payment_response = strawberry.mutation(
        resolver=create_payment_resolver)
