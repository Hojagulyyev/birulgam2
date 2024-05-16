import strawberry

from .resolvers import (
    create_deal_resolver,
    create_deal_response,
)


@strawberry.type
class DealMutations:
    create_deal: create_deal_response = strawberry.mutation(
        resolver=create_deal_resolver,
    )
