import strawberry

from .contact.resolvers import (
    get_contacts_resolver,
    get_contacts_response,
)
from .deal.resolvers import (
    get_deals_resolver,
    get_deals_response,
)


@strawberry.type
class Query:
    contacts_connection: get_contacts_response = strawberry.field(
        resolver=get_contacts_resolver)
    deals_connection: get_deals_response = strawberry.field(
        resolver=get_deals_resolver)
