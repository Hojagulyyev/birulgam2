import strawberry
 
 
@strawberry.type
class CompanySchema:
    id: int
    name: str