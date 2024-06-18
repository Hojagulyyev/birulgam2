import strawberry
 
 
@strawberry.type
class UserSessionSchema:
    user_id: int
    company_id: int
    access_token: str
