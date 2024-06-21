from application.user.usecases import (
    SigninUserUsecase,
    SignupUserUsecase,
    SignoutUserUsecase,
)

from adapters.company.repositories import CompanyPgRepository
from adapters.user.repositories import UserPgRepository
from adapters.store.repositories import StorePgRepository
from adapters.user.services import UserPasswordService
from adapters.user_session.repositories import UserSessionRedisRepository


def make_signup_user_usecase(conn):
    return SignupUserUsecase(
        user_repo=UserPgRepository(conn),
        user_password_service=UserPasswordService(),
        company_repo=CompanyPgRepository(conn),
        store_repo=StorePgRepository(conn),
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
