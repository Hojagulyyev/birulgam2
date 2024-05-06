import strawberry

from .schemas import ContactSchema
from .resolvers import get_contacts_resolver


@strawberry.type
class ContactQueries:
    contacts: list[ContactSchema] = strawberry.field(
        resolver=get_contacts_resolver,
    )
