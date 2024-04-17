import strawberry

from .schemas import Product
from .resolvers import get_products_resolver


@strawberry.type
class ProductQueries:
    products: list[Product] = strawberry.field(
        resolver=get_products_resolver)
