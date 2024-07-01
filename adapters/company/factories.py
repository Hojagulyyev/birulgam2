from application.company.usecases import (
    CreateCompanyUsecase,
)

from adapters.user.repositories import UserPgRepository
from adapters.user_session.repositories import UserSessionRedisRepository
from adapters.store.repositories import StorePgRepository
from adapters.company.repositories import CompanyPgRepository


def make_create_company_usecase(conn):
    return CreateCompanyUsecase(
        company_repo=CompanyPgRepository(conn),
        user_repo=UserPgRepository(conn),
        user_session_repo=UserSessionRedisRepository(),
        store_repo=StorePgRepository(conn),
    )
