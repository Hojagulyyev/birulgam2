import strawberry

from .resolvers import (
    get_deals_resolver,
    get_deals_response,
)


@strawberry.type
class DealQueries:
    deal_page: get_deals_response = strawberry.field(
        resolver=get_deals_resolver,
    )
