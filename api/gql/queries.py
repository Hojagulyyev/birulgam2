import strawberry

from .contact.queries import ContactQueries
from .deal.queries import DealQueries


@strawberry.type
class Query:
    contact_queries: ContactQueries = strawberry.field(resolver=ContactQueries)
    deal_queries: DealQueries = strawberry.field(resolver=DealQueries)
