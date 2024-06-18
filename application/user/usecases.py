from core.random import generate_random_string

from core.errors import DoesNotExistError, UnauthorizedError
from domain.user_session.entities import UserSession
from domain.user_session.interfaces import (
    IUserSessionRepository,
)
from domain.user.entities import User
from domain.user.interfaces import (
    IUserRepository, 
    IUserPasswordService,
)
from domain.company.entities import Company
from domain.company.interfaces import ICompanyRepository
from domain.store.entities import Store
from domain.store.interfaces import IStoreRepository

from adapters.token.services import TokenService

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
        # >>> VALIDATION
        dto.validate()

        # >>> MAIN
        hashed_password = (
            self.user_password_service
            .hash_password(dto.password)
        )
        user = User(
            id=0,
            username=dto.username,
            password=hashed_password,
        )
        user.validate()
        user = await self.user_repo.save(user)

        # >>> RESPONSE
        return user
    

class SigninUserUsecase:

    def __init__(
        self, 
        user_repo: IUserRepository,
        user_password_service: IUserPasswordService,
        user_session_repo: IUserSessionRepository,
    ):
        self.user_repo = user_repo
        self.user_password_service = user_password_service
        self.user_session_repo = user_session_repo

    async def execute(
        self, 
        dto: SigninUserUsecaseDto,
    ) -> tuple[str, UserSession]:
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

        access_token = TokenService.generate_token_by_user_id(user.id)
        user_session = UserSession(
            _user_id=user.id,
            _company_id=user.get_first_company_id(),
            _access_token=access_token,
        )
        user_session.validate()
        created_user_session = await (
            self.user_session_repo
            .set_by_access_token(access_token, user_session)
        )

        return access_token, created_user_session


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
