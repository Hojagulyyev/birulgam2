from domain.user_session.entities import UserSession
from domain.user_session.interfaces import (
    IUserSessionRepository,
)

from adapters.token.services import TokenService

from .dtos import (
    CreateUserSessionUsecaseDto,
) 


class CreateUserSessionUsecase:

    def __init__(
        self, 
        user_session_repo: IUserSessionRepository,
    ):
        self.user_session_repo = user_session_repo

    async def execute(
        self, 
        dto: CreateUserSessionUsecaseDto,
    ) -> tuple[str, UserSession]:
        access_token = TokenService.generate_token_by_user_id(dto.user_id)
        user_session = UserSession(
            _user_id=dto.user_id,
            _company_id=dto.company_id,
            _access_token=access_token,
        )
        user_session.validate()
        created_user_session = await (
            self.user_session_repo
            .set_by_access_token(access_token, user_session)
        )
        return access_token, created_user_session
