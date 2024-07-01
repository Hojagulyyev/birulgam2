from typing import Annotated

import strawberry
from strawberry.types import Info

from core.errors import Error, PermissionDeniedError
from domain.user_session.entities import UserSession

from application.company.usecases import (
    CreateCompanyUsecase,
) 
from application.company.dtos import (
    CreateCompanyUsecaseDto,
)

from adapters.user_session.repositories import UserSessionRedisRepository
from adapters.user.repositories import UserPgRepository
from adapters.company.map import CompanyMap
from adapters.company.repositories import CompanyPgRepository
from adapters.store.repositories import StorePgRepository

from ..error.schemas import ErrorSchema
from .schemas import CompanySchema
from . import inputs


create_company_response = Annotated[
    CompanySchema | ErrorSchema,
    strawberry.union('CreateCompanyResponse'),
]
async def create_company_resolver(
    info: Info,
    input: inputs.CreateCompanyInput,
) -> create_company_response:
    user_session: UserSession = info.context["user_session"]
    try:
        if user_session.company_exists():
            raise PermissionDeniedError('user already has a company')
    
        async with info.context["pgpool"].acquire() as conn:
            create_company_usecase = CreateCompanyUsecase(
                company_repo=CompanyPgRepository(conn),
                user_repo=UserPgRepository(conn),
                store_repo=StorePgRepository(conn),
                user_session_repo=UserSessionRedisRepository(),
            )
            company = await create_company_usecase.execute(
                dto=CreateCompanyUsecaseDto(
                    user_id=user_session.user_id,
                    access_token=user_session.access_token,
                    name=input.name,
                ),
            )
    except Error as e:
        return ErrorSchema(**e.serialize())

    response = CompanyMap.to_gql_schema(company)
    return response
