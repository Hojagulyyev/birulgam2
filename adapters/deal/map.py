from domain.deal.entities import Deal


class DealMap:

    @classmethod
    def serialize_one(cls, deal: Deal):
        ...

    @classmethod
    def serialize_many(cls, deals: list[Deal]):
        ...
    
    @classmethod
    def to_gql_schema(cls, deal: Deal):
        ...
