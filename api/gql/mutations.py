import strawberry

from .contact.mutations import ContactMutations
from .deal.mutations import DealMutations
from .payment.mutations import PaymentMutations


@strawberry.type
class Mutation:
    contact_mutations: ContactMutations = strawberry.field(
        resolver=ContactMutations,
    )
    deal_mutations: DealMutations = strawberry.field(
        resolver=DealMutations,
    )
    payment_mutations: PaymentMutations = strawberry.field(
        resolver=PaymentMutations,
    )