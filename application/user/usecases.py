from domain.user.entities import User
from domain.user.interfaces import (
    IUserRepository, 
    IUserPasswordService,
)

from .dtos import (
    CreateUserUsecaseDto,
) 


class GetUserByUsernameUsecase:

    def __init__(
        self, 
        user_repo: IUserRepository,
    ):
        self.user_repo = user_repo

    async def execute(self, username: str) -> User:
        user = await self.user_repo.get_by_username(username)
        return user


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
    

class CheckUserPasswordUsecase:

    def __init__(
        self, 
        user_password_service: IUserPasswordService,
    ):
        self.user_password_service = user_password_service

    async def execute(
        self, 
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        password_match = (
            self.user_password_service
            .check_password(plain_password, hashed_password)
        )
        return password_match
