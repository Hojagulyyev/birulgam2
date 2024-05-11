from fastapi import (
    FastAPI,
    Depends,
    Request,
)
import strawberry
import strawberry.exceptions
from strawberry.fastapi import GraphQLRouter

from domain.user_session.entities import UserSession

from infrastructure.fastapi.config import APP_CONFIG

from .auth import (
    get_user_session_by_authorization,
)
from .company.mutations import CompanyMutations
from .contact.queries import ContactQueries
from .contact.mutations import ContactMutations
from .deal.queries import DealQueries
from .deal.mutations import DealMutations


async def get_context(
    request: Request,
    user_session: UserSession | None = Depends(
        get_user_session_by_authorization
    ),
):
    if user_session is None:
        return {}
    
    return {
        "user_session": user_session,
        "pgpool": request.state.pgpool,
    }


@strawberry.type
class Query:
    contact_queries: ContactQueries = strawberry.field(resolver=ContactQueries)
    deal_queries: DealQueries = strawberry.field(resolver=DealQueries)


@strawberry.type
class Mutation:
    company_mutations: CompanyMutations = strawberry.field(
        resolver=CompanyMutations,
    )
    contact_mutations: ContactMutations = strawberry.field(
        resolver=ContactMutations,
    )
    deal_mutations: DealMutations = strawberry.field(
        resolver=DealMutations,
    )


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
)

app = FastAPI(**APP_CONFIG)
app.include_router(graphql_app, prefix="/graphql")
