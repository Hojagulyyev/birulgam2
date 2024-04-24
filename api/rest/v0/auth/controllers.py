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
from application.user_session.usecases import CreateUserSessionUsecase
from application.user_session.dtos import CreateUserSessionUsecaseDto

from adapters.company.repositories import CompanyPgRepository
from adapters.user.repositories import UserPgRepository
from adapters.user.map import UserMap
from adapters.user.services import UserPasswordService
from adapters.user_session.repositories import UserSessionRedisRepository

from .dtos import SignupControllerDto, SigninControllerDto


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    path="/signup",
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
        if company.id is None:
            raise TypeError

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


@router.post(
    path="/signin",
    status_code=status.HTTP_200_OK,
)
async def signin_controller(
    dto: SigninControllerDto,
):
    # TODO: get user by username
    user = {
        "id": 1,
        "company_id": 1,
    }

    create_user_session_usecase = CreateUserSessionUsecase(
        user_session_repo=UserSessionRedisRepository(),
    )
    access_token, user_session = await create_user_session_usecase.execute(
        CreateUserSessionUsecaseDto(
            user_id=user["id"],
            company_id=user["company_id"],
        )
    )
    return access_token, user_session
