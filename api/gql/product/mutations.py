import strawberry
from strawberry.field_extensions import InputMutationExtension

from .schemas import Product
from .resolvers import create_product_resolver


@strawberry.type
class ProductMutations:
    create_product: Product = strawberry.mutation(
        resolver=create_product_resolver,
    )
