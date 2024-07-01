from application.user_session.usecases import (
    CreateUserSessionUsecase,
)

from adapters.user_session.repositories import UserSessionRedisRepository


def make_create_user_session_usecase():
    return CreateUserSessionUsecase(
        user_session_repo=UserSessionRedisRepository(),
    )
