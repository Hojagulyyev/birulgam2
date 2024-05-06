from strawberry.types import Info

from application.company.usecases import (
    CreateCompanyUsecase,
) 
from application.company.dtos import (
    CreateCompanyUsecaseDto,
)
from adapters.company.map import CompanyMap
from adapters.company.repositories import CompanyPgRepository

from .schemas import CompanySchema
from . import inputs


async def create_company_resolver(
    info: Info,
    input: inputs.CreateCompanyInput,
) -> CompanySchema:
    async with info.context["pgpool"].acquire() as conn:
        company_repo = CompanyPgRepository(conn=conn)
        create_company_usecase = CreateCompanyUsecase(
            company_repo=company_repo,
        )
        company = await create_company_usecase.execute(
            CreateCompanyUsecaseDto(name=input.name),
        )
    response = CompanyMap.to_gql_schema(company)
    return response
