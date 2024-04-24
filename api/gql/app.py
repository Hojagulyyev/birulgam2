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
from api.http.auth import (
    get_user_session_by_authorization_for_gql,
)

from .company.mutations import CompanyMutations
from .company.schemas import CompanySchema


async def get_context(
    request: Request,
    user_session: UserSession | None = Depends(
        get_user_session_by_authorization_for_gql
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


@strawberry.type
class Mutation:
    company_mutations: CompanyMutations = strawberry.field(
        resolver=CompanyMutations,
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
