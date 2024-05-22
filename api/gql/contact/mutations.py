import strawberry

from ..error.schemas import ErrorSchema
from .schemas import ContactSchema
from .resolvers import create_contact_resolver


@strawberry.type
class ContactMutations:
    create_contact: ContactSchema | ErrorSchema = strawberry.mutation(
        resolver=create_contact_resolver,
    )
