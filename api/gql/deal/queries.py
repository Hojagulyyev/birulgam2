import strawberry

from .schemas import DealPageSchema
from .resolvers import get_deals_resolver


@strawberry.type
class DealQueries:
    deal_page: DealPageSchema = strawberry.field(
        resolver=get_deals_resolver,
    )
