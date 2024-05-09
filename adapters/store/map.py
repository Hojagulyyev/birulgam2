from domain.store.entities import Store


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
