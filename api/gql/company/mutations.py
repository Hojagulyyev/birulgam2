import strawberry

from .schemas import CompanySchema
from .resolvers import (
    create_company_resolver,
)


@strawberry.type
class CompanyMutations:
    create_company: CompanySchema = strawberry.mutation(
        resolver=create_company_resolver,
    )
