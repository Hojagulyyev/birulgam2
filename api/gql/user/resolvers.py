from typing import Annotated

import strawberry
from strawberry.types import Info

from core.errors import Error, DoesNotExistError
from core.random import generate_random_string
from domain.user_session.entities import UserSession

from application.user.dtos import (
    SigninUserUsecaseDto,
    SignoutUserUsecaseDto,
    CreateUserUsecaseDto,
)
from application.user.usecases import (
    GetUserByPhoneUsecase,
)
from application.user_session.usecases import CreateUserSessionUsecase
from application.user_session.dtos import CreateUserSessionUsecaseDto
from application.otp.usecases import (
    ExistOtpUsecase,
    ExistOtpUsecaseDto,
)

from adapters.user.factories import (
    make_create_user_usecase,
    make_signin_user_usecase,
    make_signout_user_usecase,
)
from adapters.user_session.map import UserSessionMap
from adapters.user.map import UserMap
from adapters.user.repositories import UserPgRepository
from adapters.user_session.repositories import UserSessionRedisRepository

from ..error.schemas import ErrorSchema
from ..user_session.schemas import UserSessionSchema
from .schemas import UserSchema
from .inputs import (
    SignupUserInput,
    SigninUserInput,
    SigninByOtpUserInput,
)


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


signout_user_response = Annotated[
    UserSessionSchema | ErrorSchema,
    strawberry.union('SignoutUserResponse'),
]
async def signout_user_resolver(
    info: Info,
) -> signout_user_response:
    user_session: UserSession = info.context["user_session"]
    try:
        signout_user_usecase = make_signout_user_usecase()
        await signout_user_usecase.execute(
            dto=SignoutUserUsecaseDto(
                access_token=user_session.access_token,
            )
        )
    except Error as e:
        return ErrorSchema(**e.serialize())
    
    user_session_schema = UserSessionMap.to_gql_schema(user_session)
    return user_session_schema
    

signin_user_by_otp_response = Annotated[
    UserSessionSchema | ErrorSchema,
    strawberry.union('SigninUserResponse'),
]
async def signin_user_by_otp_resolver(
    info: Info,
    input: SigninByOtpUserInput,
) -> signin_user_by_otp_response:
    try:
        otp_exists = await ExistOtpUsecase().execute(
            dto=ExistOtpUsecaseDto(input.phone, input.otp),
        )
        if not otp_exists:
            return ErrorSchema(
                loc=['input', 'otp'], 
                type='does_not_exist',
            )
    
        async with info.context["pgpool"].acquire() as conn:
            get_user_by_phone_usecase = GetUserByPhoneUsecase(
                UserPgRepository(conn=conn),
            )
            try:
                user = await get_user_by_phone_usecase.execute(input.phone)
            except DoesNotExistError:
                signup_user_usecase = make_create_user_usecase(conn)
                random_generated_password = generate_random_string()
                user = await signup_user_usecase.execute(
                    dto=CreateUserUsecaseDto(
                        username=input.phone,
                        password=random_generated_password,
                        phone=input.phone,
                        company_ids=[],
                    )
                )

        create_user_session_usecase = CreateUserSessionUsecase(
            user_session_repo=UserSessionRedisRepository(),
        )
        user_session = await create_user_session_usecase.execute(
            CreateUserSessionUsecaseDto(
                user_id=user.id,
                company_id=user.get_first_company_id(),
            ),
        )

    except Error as e:
        return ErrorSchema(**e.serialize())
    
    user_session_schema = UserSessionMap.to_gql_schema(user_session)
    return user_session_schema
