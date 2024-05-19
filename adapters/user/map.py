from domain.user.entities import User

from adapters.company.map import CompanyMap
from api.gql.user.schemas import UserSchema


class UserMap:

    @classmethod
    def serialize_one(cls, user: User):
        return {
            "id": user.id,
            "username": user.username,
            "companies": (
                user.companies and [
                    CompanyMap.serialize_one(company)
                    for company in user.companies
                ]
            ),
        }

    @classmethod
    def serialize_many(cls, users: list[User]):
        return [ 
            UserMap.serialize_one(user) 
            for user in users 
        ]
    
    @classmethod
    def to_gql_schema(cls, user: User):
        if user.id is None:
            raise TypeError
        
        return UserSchema(
            id=user.id,
            username=user.username,
            company_ids=user.company_ids,
            companies=(
                user.companies and [
                    CompanyMap.to_gql_schema(company)
                    for company in user.companies
                ]
            ), # type: ignore
        )
