import strawberry

from .resolvers import (
    get_contacts_resolver,
    get_contacts_response,
)


@strawberry.type
class ContactQueries:
    contact_page: get_contacts_response = strawberry.field(
        resolver=get_contacts_resolver,
    )
