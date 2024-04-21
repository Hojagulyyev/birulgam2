from domain.company.entities import Company

from api.gql.company.schemas import CompanySchema


class CompanyMap:

    @classmethod
    def serialize_one(cls, company: Company):
        return company.__dict__

    @classmethod
    def serialize_many(cls, companies: list[Company]):
        return [ 
            CompanyMap.serialize_one(company) 
            for company in companies 
        ]
    
    @classmethod
    def to_gql_schema(cls, company: Company):
        return CompanySchema(
            id=company.id,
            name=company.name,
        )
