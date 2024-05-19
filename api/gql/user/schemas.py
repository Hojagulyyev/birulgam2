import strawberry

from ..company.schemas import CompanySchema
 
 
@strawberry.type
class UserSchema:
    id: int
    username: str

    company_ids: list[int] | None = None
    companies: list[CompanySchema] | None = None
