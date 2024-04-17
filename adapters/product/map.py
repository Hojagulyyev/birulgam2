from domain.product.entities import Product

from api.gql.product.schemas import Product as ProductGqlSchema


class ProductMap:

    @classmethod
    def serialize_one(cls, product: Product):
        return product.__dict__

    @classmethod
    def serialize_many(cls, products: list[Product]):
        return [ ProductMap.serialize_one(product) for product in products ]
    
    @classmethod
    def to_gql_schema(cls, product: Product):
        return ProductGqlSchema(
            id=product.id,
            name=product.name,
        )
    