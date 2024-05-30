from fastapi import (
    APIRouter,
    status,
    Request,
    HTTPException,
)
from fastapi.responses import JSONResponse

from core.errors import Error, DoesNotExistError
from core.random import generate_otp, generate_random_string

from application.user.usecases import (
    GetUserByUsernameUsecase,
)
from application.user.dtos import SignupUserUsecaseDto, SigninUserUsecaseDto
from application.user_session.usecases import CreateUserSessionUsecase
from application.user_session.dtos import CreateUserSessionUsecaseDto

from adapters.user.factories import (
    make_signin_user_usecase,
    make_signup_user_usecase,
)
from adapters.user_session.map import UserSessionMap
from adapters.otp.repositories import OtpRedisRepository
from adapters.user.repositories import UserPgRepository
from adapters.user.map import UserMap
from adapters.user_session.repositories import UserSessionRedisRepository

from .dtos import (
    SignupControllerDto, 
    SigninControllerDto,
    SendOtpControllerDto,
    SigninByOtpControllerDto,
)


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
        signup_user_usecase = make_signup_user_usecase(conn)
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
    try:
        async with request.state.pgpool.acquire() as conn:
            signin_user_usecase = make_signin_user_usecase(conn)
            user = await signin_user_usecase.execute(
                dto=SigninUserUsecaseDto(
                    username=dto.username,
                    password=dto.password,
                )
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
    except Error as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.serialize(),
        )
    
    return {
        'access_token': access_token, 
        'user_session': UserSessionMap.serialize_one(user_session),
    }


# TODO: send otp to phone via email or sms service
@router.post(
    path="/otp",
    status_code=status.HTTP_200_OK,
)
async def send_otp_controller(
    dto: SendOtpControllerDto,
):
    otp = generate_otp()
    otp_repo = OtpRedisRepository()
    otp_repo.set_by_phone(dto.phone, otp)
    # otp_service.send_otp(otp) implement this service
    print('otp', otp)
    return {
        'phone': dto.phone
    }


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
    otp_repo = OtpRedisRepository()
    otp = otp_repo.get_by_phone(dto.phone)

    if not otp or otp != dto.otp:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="invalid otp",
        )
    
    try:
        async with request.state.pgpool.acquire() as conn:
            get_user_by_username_usecase = GetUserByUsernameUsecase(
                UserPgRepository(conn=conn),
            )
            try:
                user = await get_user_by_username_usecase.execute(dto.phone)
            except DoesNotExistError:
                # >>> SIGNUP
                signup_user_usecase = make_signup_user_usecase(conn)

                random_generated_password = generate_random_string()
                user = await signup_user_usecase.execute(
                    dto=SignupUserUsecaseDto(
                        username=dto.phone,
                        password=random_generated_password,
                        password_confirm=random_generated_password,
                        create_company=False,
                    )
                )
                return JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    content=UserMap.serialize_one(user),
                )
            
        # >>> SIGNIN
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

    except Error as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.serialize(),
        )
    
    return {
        'access_token': access_token, 
        'user_session': UserSessionMap.serialize_one(user_session),
    }
