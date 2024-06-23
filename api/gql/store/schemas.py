import strawberry

from ..company.schemas import CompanySchema
 
 
@strawberry.type
class StoreSchema:
    id: int
    company_id: int

    name: str
    code: str

    company: CompanySchema | None = None


@strawberry.type
class StoresConnectionSchema:
    stores: list[StoreSchema]
    total: int
