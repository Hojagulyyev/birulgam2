import strawberry

from ..company.schemas import CompanySchema
 
 
@strawberry.type
class UserSchema:
    id: int
    company_ids: list[int]
    
    username: str

    companies: list[CompanySchema] | None = None
