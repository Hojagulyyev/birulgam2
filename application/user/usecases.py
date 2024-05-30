from core.random import generate_random_string

from core.errors import DoesNotExistError, UnauthorizedError
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
    SigninUserUsecaseDto,
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
        # >>> VALIDATE
        dto.validate()

        # >>> MAIN
        companies: list[Company] = []
        if dto.create_company:
            company = Company(
                id=0, 
                name=generate_random_string(),
            )
            company.validate()
            company = await self.company_repo.save(company)
            companies.append(company)
            
            store = Store(
                id=0,
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
            id=0,
            username=dto.username,
            password=hashed_password,
            company_ids=[company.id for company in companies],
        )
        user.validate()
        user = await self.user_repo.save(user)

        # >>> RESPONSE
        user.companies = companies
        return user
    

class SigninUserUsecase:

    def __init__(
        self, 
        user_repo: IUserRepository,
        user_password_service: IUserPasswordService,
    ):
        self.user_repo = user_repo
        self.user_password_service = user_password_service

    async def execute(self, dto: SigninUserUsecaseDto) -> User:
        user = await self.user_repo.get_by_username(dto.username)
        if not user:
            raise DoesNotExistError(loc=['user', 'username'])

        password_match = (
            self.user_password_service
            .check_password(dto.password, user.password)
        )
        if not password_match:
            raise UnauthorizedError('invalid authentication credentials')
        
        await self.user_repo.join_companies(user)
        return user


class GetUserByUsernameUsecase:

    def __init__(
        self, 
        user_repo: IUserRepository,
    ):
        self.user_repo = user_repo

    async def execute(self, username: str) -> User:
        user = await self.user_repo.get_by_username(username)
        if not user:
            raise DoesNotExistError(loc=['user', 'username'])
        
        await self.user_repo.join_companies(user)
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
            id=0,
            username=dto.username,
            password=hashed_password,
            company_ids=dto.company_ids,
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
