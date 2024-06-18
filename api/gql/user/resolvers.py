from typing import Annotated

import strawberry
from strawberry.types import Info

from core.errors import Error
from domain.user_session.entities import UserSession

from application.user.dtos import (
    SignupUserUsecaseDto, 
    SigninUserUsecaseDto,
)
from adapters.user.factories import (
    make_signin_user_usecase,
    make_signup_user_usecase,
)
from adapters.user.map import UserMap
from adapters.user.repositories import UserPgRepository

from ..error.schemas import ErrorSchema
from .schemas import UserSchema
from .inputs import (
    SignupUserInput,
)


signup_user_response = Annotated[
    UserSchema | ErrorSchema,
    strawberry.union('SignupUserResponse'),
]
async def signup_user_resolver(
    info: Info,
    input: SignupUserInput,
) -> signup_user_response:
    try:
        async with info.context["pgpool"].acquire() as conn:
            signup_user_usecase = make_signup_user_usecase(conn)
            user = await signup_user_usecase.execute(
                dto=SignupUserUsecaseDto(
                    username=input.username,
                    password=input.password,
                    password_confirm=input.password_confirm,
                )
            )
    except Error as e:
        return ErrorSchema(**e.serialize())
    
    user_schema = UserMap.to_gql_schema(user)
    return user_schema
