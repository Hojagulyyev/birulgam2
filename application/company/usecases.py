from domain.company.entities import Company
from domain.company.interfaces import ICompanyRepository

from .dtos import (
    CreateCompanyUsecaseDto,
) 


class CreateCompanyUsecase:

    def __init__(self, company_repo: ICompanyRepository):
        self.company_repo = company_repo

    def execute(self, dto: CreateCompanyUsecaseDto) -> Company:
        company = Company(name=dto.name)
        created_company = self.company_repo.save(company)
        return created_company
