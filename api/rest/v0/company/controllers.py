from fastapi import (
    APIRouter,
    Depends,
    status,
)
from asyncpg import Pool

from application.company.usecases import (
    CreateCompanyUsecase,
) 
from application.company.dtos import (
    CreateCompanyUsecaseDto,
)
from adapters.company.repositories import CompanyPgRepository
from adapters.company.map import CompanyMap
from infrastructure.postgres import get_pool

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
def create_company_controller(
    dto: CreateCompanyControllerDto,
    pool: Pool = Depends(get_pool)
):
    with pool.acquire() as conn:
        company_repo = CompanyPgRepository(conn=conn)
        create_company_usecase = CreateCompanyUsecase(
            company_repo=company_repo,
        )
        company = create_company_usecase.execute(
            CreateCompanyUsecaseDto(name=dto.name),
        )
    
    response = CompanyMap.serialize_one(company)
    return response
