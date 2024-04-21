from domain.user.entities import User
from domain.user.interfaces import (
    IUserRepository, 
    IUserPasswordService,
)

from .dtos import (
    CreateUserUsecaseDto,
) 


class CreateUserUsecase:

    def __init__(
        self, 
        user_repo: IUserRepository,
        user_password_service: IUserPasswordService,
    ):
        self.user_repo = user_repo
        self.user_password_service = user_password_service

    async def execute(self, dto: CreateUserUsecaseDto) -> User:
        hashed_password = (
            self.user_password_service
            .hash_password(dto.password)
        )
        user = User(
            username=dto.username,
            password=hashed_password,
            company_id=dto.company_id,
        )
        created_user = await self.user_repo.save(user)
        return created_user
