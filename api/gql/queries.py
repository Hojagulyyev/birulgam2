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
    contact_page: get_contacts_response = strawberry.field(
        resolver=get_contacts_resolver)
    deal_page: get_deals_response = strawberry.field(
        resolver=get_deals_resolver)
