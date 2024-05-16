from core.random import generate_random_string

from domain.user.entities import User
from domain.user.interfaces import (
    IUserRepository, 
    IUserPasswordService,
)
from domain.company.entities import Company
from domain.company.interfaces import ICompanyRepository
from domain.store.entities import Store
from domain.store.interfaces import IStoreRepository

from .dtos import (
    SignupUserUsecaseDto,
    CreateUserUsecaseDto,
)


class SignupUserUsecase:

    def __init__(
        self, 
        user_repo: IUserRepository,
        user_password_service: IUserPasswordService,
        company_repo: ICompanyRepository,
        store_repo: IStoreRepository,
    ):
        self.user_repo = user_repo
        self.user_password_service = user_password_service
        self.company_repo = company_repo
        self.store_repo = store_repo

    async def execute(self, dto: SignupUserUsecaseDto) -> User:
        dto.validate()

        company = Company(name=generate_random_string())
        company.validate()
        company = await self.company_repo.save(company)
        if company.id is None:
            raise TypeError
        
        store = Store(
            company_id=company.id,
            name=generate_random_string(),
            code=generate_random_string(Store.CODE_MAX_LENGTH),
        )
        store.validate()
        store = await self.store_repo.save(store)

        hashed_password = (
            self.user_password_service
            .hash_password(dto.password)
        )
        user = User(
            username=dto.username,
            password=hashed_password,
            company_id=company.id,
        )
        user.validate()
        user = await self.user_repo.save(user)
        user.company = company
        return user


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
        user.validate()
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
