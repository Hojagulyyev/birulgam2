from typing import Annotated

import strawberry
from strawberry.types import Info

from core.errors import Error, DoesNotExistError
from core.random import generate_random_string
from core.phone import format_phone
from domain.user_session.entities import UserSession

from application.user.dtos import (
    SigninUserUsecaseDto,
    SignoutUserUsecaseDto,
    CreateUserUsecaseDto,
)
from application.user_session.dtos import CreateUserSessionUsecaseDto
from application.otp.usecases import (
    ExistOtpUsecase,
    ExistOtpUsecaseDto,
)
from application.company.dtos import CreateCompanyUsecaseDto

from adapters.user.factories import (
    make_create_user_usecase,
    make_signin_user_usecase,
    make_signout_user_usecase,
    make_get_user_by_phone_usecase,
)
from adapters.company.factories import make_create_company_usecase
from adapters.user_session.factories import make_create_user_session_usecase
from adapters.user_session.map import UserSessionMap

from ..error.schemas import ErrorSchema
from ..user_session.schemas import UserSessionSchema
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
            try:
                user = await (
                    make_get_user_by_phone_usecase(conn)
                    .execute(input.phone)
                )
            except DoesNotExistError:
                user = await (
                    make_create_user_usecase(conn)
                    .execute(
                        dto=CreateUserUsecaseDto(
                            username=format_phone(input.phone),
                            password=generate_random_string(),
                            phone=input.phone,
                            company_ids=[],
                        )
                    )
                )

            user_session = await (
                make_create_user_session_usecase()
                .execute(
                    CreateUserSessionUsecaseDto(
                        user_id=user.id,
                        company_id=user.get_first_company_id(),
                    ),
                )
            )
            
            if not user.companies:
                company = await (
                    make_create_company_usecase(conn)
                    .execute(
                        dto=CreateCompanyUsecaseDto(
                            user_id=user.id,
                            access_token=user_session.access_token,
                            name=user.username,
                        )
                    )
                )
                company_id = company.id
            else:
                company_id = user.get_first_company_id()
    except Error as e:
        return ErrorSchema(**e.serialize())
    
    user_session_schema = UserSessionMap.to_gql_schema(user_session)
    user_session_schema.company_id = company_id
    return user_session_schema
