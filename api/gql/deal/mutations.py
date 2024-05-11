import strawberry

from .schemas import DealSchema
from .resolvers import create_deal_resolver


@strawberry.type
class DealMutations:
    create_deal: DealSchema = strawberry.mutation(
        resolver=create_deal_resolver,
    )
