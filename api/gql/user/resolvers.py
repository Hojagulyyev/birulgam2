from typing import Annotated

import strawberry
from strawberry.types import Info

from core.errors import Error

from application.user.dtos import (
    SignupUserUsecaseDto, 
    SigninUserUsecaseDto,
)

from adapters.user.factories import (
    make_signin_user_usecase,
    make_signup_user_usecase,
)
from adapters.user_session.map import UserSessionMap
from adapters.user.map import UserMap

from ..error.schemas import ErrorSchema
from ..user_session.schemas import UserSessionSchema
from .schemas import UserSchema
from .inputs import (
    SignupUserInput,
    SigninUserInput,
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


signin_user_response = Annotated[
    UserSessionSchema | ErrorSchema,
    strawberry.union('SigninUserResponse'),
]
async def signin_user_resolver(
    info: Info,
    input: SigninUserInput,
) -> signin_user_response:
    try:
        async with info.context["pgpool"].acquire() as conn:
            signin_user_usecase = make_signin_user_usecase(conn)
            user_session = await signin_user_usecase.execute(
                dto=SigninUserUsecaseDto(
                    username=input.username,
                    password=input.password,
                )
            )
    except Error as e:
        return ErrorSchema(**e.serialize())
    
    user_session_schema = UserSessionMap.to_gql_schema(user_session)
    return user_session_schema
