from fastapi import (
    APIRouter,
    status,
    Request,
    HTTPException,
)

from core.errors import Error

from application.user.usecases import (
    GetUserByUsernameUsecase,
    CheckUserPasswordUsecase,
    SignupUserUsecase,
)
from application.user.dtos import SignupUserUsecaseDto
from application.user_session.usecases import CreateUserSessionUsecase
from application.user_session.dtos import CreateUserSessionUsecaseDto

from adapters.company.repositories import CompanyPgRepository
from adapters.user.repositories import UserPgRepository
from adapters.store.repositories import StorePgRepository
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
        signup_user_usecase = SignupUserUsecase(
            user_repo=UserPgRepository(conn),
            user_password_service=UserPasswordService(),
            company_repo=CompanyPgRepository(conn),
            store_repo=StorePgRepository(conn),
        )
        try:
            user = await signup_user_usecase.execute(
                dto=SignupUserUsecaseDto(
                    username=dto.username,
                    password=dto.password,
                    password_confirm=dto.password_confirm,
                    create_company=dto.create_company,
                )
            )
        except Error as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=e.serialize(),
            )

    response = UserMap.serialize_one(user)
    return response


@router.post(
    path="/signin",
    status_code=status.HTTP_200_OK,
)
async def signin_controller(
    dto: SigninControllerDto,
    request: Request,
):
    async with request.state.pgpool.acquire() as conn:
        # TODO: move below validation logics into create user session usecase
        get_user_by_username_usecase = GetUserByUsernameUsecase(
            UserPgRepository(conn=conn),
        )
        try:
            user = await get_user_by_username_usecase.execute(dto.username)
        except Error as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=e.serialize(),
            )
    
    check_user_password_usecase = CheckUserPasswordUsecase(
        user_password_service=UserPasswordService()
    )
    password_match = await (
        check_user_password_usecase
        .execute(dto.password, user.password)
    )
    if not password_match:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="invalid authentication credentials",
        )

    create_user_session_usecase = CreateUserSessionUsecase(
        user_session_repo=UserSessionRedisRepository(),
    )

    if not user.companies:
        company_id: int = 0
    else:
        company_id: int = user.companies[0].id if len(user.companies) else 0

    access_token, user_session = await create_user_session_usecase.execute(
        CreateUserSessionUsecaseDto(
            user_id=user.id,
            company_id=company_id,
        ),
    )
    return {
        'access_token': access_token, 
        'user_session': {
            'user_id': user_session.user_id,
            'company_id': user_session.company_id,
        }
    }
