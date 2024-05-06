import strawberry

from .schemas import ContactPageSchema
from .resolvers import get_contacts_resolver


@strawberry.type
class ContactQueries:
    contact_page: ContactPageSchema = strawberry.field(
        resolver=get_contacts_resolver,
    )
