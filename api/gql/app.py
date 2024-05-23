from fastapi import FastAPI
import strawberry
import strawberry.exceptions
from strawberry.fastapi import GraphQLRouter

from infrastructure.fastapi.config import APP_CONFIG

from .queries import Query
from .mutations import Mutation
from .context import get_context


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
