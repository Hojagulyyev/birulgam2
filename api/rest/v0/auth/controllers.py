from fastapi import (
    APIRouter,
    Depends,
    status,
    Request,
    HTTPException,
)
from asyncpg.exceptions import UniqueViolationError

from application.company.usecases import CreateCompanyUsecase
from application.company.dtos import CreateCompanyUsecaseDto
from application.user.usecases import CreateUserUsecase
from application.user.dtos import CreateUserUsecaseDto

from adapters.company.repositories import CompanyPgRepository
from adapters.user.repositories import UserPgRepository
from adapters.user.map import UserMap
from adapters.user.services import UserPasswordService

from .dtos import SignupControllerDto


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
)
async def signup_controller(
    dto: SignupControllerDto,
    request: Request,
):
    async with request.state.pgpool.acquire() as conn:
        company_repo = CompanyPgRepository(conn=conn)
        create_company_usecase = CreateCompanyUsecase(company_repo)
        company = await create_company_usecase.execute(
            CreateCompanyUsecaseDto(),
        )
        

        user_repo = UserPgRepository(conn=conn)
        create_user_usecase = CreateUserUsecase(
            user_repo=user_repo, 
            user_password_service=UserPasswordService(),
        )
        try:
            user = await create_user_usecase.execute(
                CreateUserUsecaseDto(
                    username=dto.username,
                    password=dto.password,
                    company_id=company.id,
                )
            )
        except UniqueViolationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e),
            )

    user.company = company
    response = UserMap.serialize_one(user)
    return response
