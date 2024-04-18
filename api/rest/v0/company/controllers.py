from fastapi import (
    APIRouter,
    Depends,
    status,
    Request,
)

from application.company.usecases import (
    CreateCompanyUsecase,
) 
from application.company.dtos import (
    CreateCompanyUsecaseDto,
)
from adapters.company.repositories import CompanyPgRepository
from adapters.company.map import CompanyMap

from .dtos import (
    CreateCompanyControllerDto,
)


router = APIRouter(
    prefix="/companies",
    tags=["companies"],
)


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
)
async def create_company_controller(
    dto: CreateCompanyControllerDto,
    request: Request,
):
    async with request.state.pgpool.acquire() as conn:
        company_repo = CompanyPgRepository(conn=conn)
        create_company_usecase = CreateCompanyUsecase(
            company_repo=company_repo,
        )
        company = await create_company_usecase.execute(
            CreateCompanyUsecaseDto(name=dto.name),
        )

    response = CompanyMap.serialize_one(company)
    return response
