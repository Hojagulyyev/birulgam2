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
    contacts: get_contacts_response = strawberry.field(
        resolver=get_contacts_resolver)
    deals: get_deals_response = strawberry.field(
        resolver=get_deals_resolver)
