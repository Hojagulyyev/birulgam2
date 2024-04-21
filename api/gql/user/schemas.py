import strawberry

from ..company.schemas import CompanySchema
 
 
@strawberry.type
class UserSchema:
    id: int
    username: str
    company_id: int
    company: CompanySchema | None
