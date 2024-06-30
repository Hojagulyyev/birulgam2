from application.user.usecases import (
    SigninUserUsecase,
    SignoutUserUsecase,
    CreateUserUsecase,
)

from adapters.user.repositories import UserPgRepository
from adapters.user.services import UserPasswordService
from adapters.user_session.repositories import UserSessionRedisRepository


def make_create_user_usecase(conn):
    return CreateUserUsecase(
        user_repo=UserPgRepository(conn),
        user_password_service=UserPasswordService(),
    )


def make_signin_user_usecase(conn):
    return SigninUserUsecase(
        user_repo=UserPgRepository(conn),
        user_password_service=UserPasswordService(),
        user_session_repo=UserSessionRedisRepository(),
    )


def make_signout_user_usecase():
    return SignoutUserUsecase(
        user_session_repo=UserSessionRedisRepository(),
    )
