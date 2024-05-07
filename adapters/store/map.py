from domain.store.entities import Store

from adapters.company.map import CompanyMap
# from api.gql.store.schemas import StoreSchema


class StoreMap:

    @classmethod
    def serialize_one(cls, store: Store):
        ...

    @classmethod
    def serialize_many(cls, stores: list[Store]):
        ...
    
    @classmethod
    def to_gql_schema(cls, store: Store):
        ...
