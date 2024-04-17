from strawberry.types import Info

from application.product.usecases import (
    GetProductsUsecase,
    CreateProductUsecase,
) 
from application.product.dtos import (
    GetProductsUsecaseDto,
    CreateProductUsecaseDto,
)
from adapters.product.map import ProductMap
from adapters.product.repositories import ProductSqliteRepository

from .schemas import Product
from . import inputs


def get_products_resolver(
    info: Info,
    input: inputs.GetProductsInput | None = None,
):
    with info.context["sqlite_conn"] as conn:
        product_repo = ProductSqliteRepository(conn=conn)
        get_products_usecase = GetProductsUsecase(
            product_repo=product_repo,
        )
        products = get_products_usecase.execute(GetProductsUsecaseDto())
    
    response = [ProductMap.to_gql_schema(product) for product in products]
    return response


def create_product_resolver(
    self,
    info: Info,
    input: inputs.CreateProductInput,
) -> Product:
    with info.context["sqlite_conn"] as conn:
        product_repo = ProductSqliteRepository(conn=conn)
        create_product_usecase = CreateProductUsecase(
            product_repo=product_repo,
        )
        product = create_product_usecase.execute(
            CreateProductUsecaseDto(name=input.name),
        )
    response = ProductMap.to_gql_schema(product)
    return response
