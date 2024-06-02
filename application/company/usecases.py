from core.errors import DoesNotExistError
from domain.company.entities import Company
from domain.company.interfaces import ICompanyRepository
from domain.user.interfaces import IUserRepository
from domain.user_session.interfaces import IUserSessionRepository

from .dtos import (
    CreateCompanyUsecaseDto,
) 


class CreateCompanyUsecase:

    def __init__(
        self,
        company_repo: ICompanyRepository,
        user_repo: IUserRepository,
        user_session_repo: IUserSessionRepository,

    ):
        self.company_repo = company_repo
        self.user_session_repo = user_session_repo
        self.user_repo = user_repo

    async def execute(self, dto: CreateCompanyUsecaseDto) -> Company:
        company = Company(
            id=0,
            name=dto.name,
        )
        company.validate()
        created_company = await self.company_repo.save(company)

        user = await self.user_repo.get_by_id(dto.user_id)
        if not user:
            raise DoesNotExistError(loc=['user', 'id'])
        user.company_ids = [company.id]
        await self.user_repo.save(user)

        user_session = await self.user_session_repo.get_by_access_token(dto.access_token)
        user_session.company_id = company.id
        await self.user_session_repo.set_by_access_token(dto.access_token, user_session)

        return created_company
