import strawberry

from .resolvers import (
    create_contact_resolver,
    create_contact_response,
)


@strawberry.type
class ContactMutations:
    create_contact: create_contact_response = strawberry.mutation(
        resolver=create_contact_resolver,
    )
