from domain.user_session.entities import UserSession
from domain.user_session.interfaces import (
    IUserSessionRepository,
)

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
    ) -> UserSession:
        
        user_session = UserSession(
            user_id=dto.user_id,
            company_id=dto.company_id,
        )
        created_user_session = await (
            self.user_session_repo
            .save(user_session)
        )
        return created_user_session
