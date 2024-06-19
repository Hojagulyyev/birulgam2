from fastapi import (
    APIRouter,
    status,
    Request,
    HTTPException,
)

from core.errors import Error, DoesNotExistError
from core.random import generate_random_string

from application.user.usecases import (
    GetUserByUsernameUsecase,
)
from application.user.dtos import SignupUserUsecaseDto
from application.user_session.usecases import CreateUserSessionUsecase
from application.user_session.dtos import CreateUserSessionUsecaseDto
from application.otp.usecases import (
    SendOtpUsecase,
    SendOtpUsecaseDto,
    ExistOtpUsecase,
    ExistOtpUsecaseDto,
)

from adapters.user.factories import make_signup_user_usecase
from adapters.user_session.map import UserSessionMap
from adapters.otp.repositories import OtpRedisRepository
from adapters.user.repositories import UserPgRepository
from adapters.user_session.repositories import UserSessionRedisRepository

from .dtos import (
    SendOtpControllerDto,
    SigninByOtpControllerDto,
)


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


# TODO: use below controller as gql resolver
# TODO: send otp to phone via email or sms service
@router.post(
    path="/otp",
    status_code=status.HTTP_200_OK,
)
async def send_otp_controller(
    dto: SendOtpControllerDto,
):
    phone = await SendOtpUsecase().execute(SendOtpUsecaseDto(dto.phone))
    return {
        'phone': dto.phone
    }


# TODO: use below controller as gql resolver
@router.post(
    path="/signin-otp",
    responses={
        status.HTTP_201_CREATED: {"model": {}},
        status.HTTP_200_OK: {'model': {}},
    },
)
async def signin_by_otp_controller(
    dto: SigninByOtpControllerDto,
    request: Request,
):  
    otp_exists = await ExistOtpUsecase().execute(
        dto=ExistOtpUsecaseDto(dto.phone, dto.otp),
    )
    if not otp_exists:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='otp does not exist',
        )

    try:
        async with request.state.pgpool.acquire() as conn:
            get_user_by_username_usecase = GetUserByUsernameUsecase(
                UserPgRepository(conn=conn),
            )
            try:
                user = await get_user_by_username_usecase.execute(dto.phone)
            except DoesNotExistError:
                signup_user_usecase = make_signup_user_usecase(conn)
                random_generated_password = generate_random_string()
                user = await signup_user_usecase.execute(
                    dto=SignupUserUsecaseDto(
                        username=dto.phone,
                        password=random_generated_password,
                        password_confirm=random_generated_password,
                    )
                )
            
        create_user_session_usecase = CreateUserSessionUsecase(
            user_session_repo=UserSessionRedisRepository(),
        )
        access_token, user_session = await create_user_session_usecase.execute(
            CreateUserSessionUsecaseDto(
                user_id=user.id,
                company_id=user.get_first_company_id(),
            ),
        )
    except Error as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.serialize(),
        )
    
    return {
        'access_token': access_token, 
        'user_session': UserSessionMap.serialize_one(user_session),
    }
