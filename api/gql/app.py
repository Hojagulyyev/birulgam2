from fastapi import (
    FastAPI, 
    Depends, 
    HTTPException, 
    Request, 
    status,
    Body,
)
import strawberry
import strawberry.exceptions
from strawberry.fastapi import GraphQLRouter

from domain.user_session.entities import UserSession

from infrastructure.fastapi.config import APP_CONFIG

from .auth import (
    get_user_session_by_authorization,
)
from .company.schemas import CompanySchema
from .company.mutations import CompanyMutations
from .contact.schemas import ContactSchema
from .contact.queries import ContactQueries
from .contact.mutations import ContactMutations


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


def get_companies() -> list[CompanySchema]:
    return [CompanySchema(id=1, name="BirUlgam2"),]

@strawberry.type
class Query:
    companies: list[CompanySchema] = strawberry.field(resolver=get_companies)
    contact_queries: ContactQueries = strawberry.field(resolver=ContactQueries)


@strawberry.type
class Mutation:
    company_mutations: CompanyMutations = strawberry.field(
        resolver=CompanyMutations,
    )
    contact_mutations: ContactMutations = strawberry.field(
        resolver=ContactMutations,
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
