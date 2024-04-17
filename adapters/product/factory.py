from application.product import usecases

from . import repositories


def make_product_list_repository() -> repositories.ProductListRepository:
    return repositories.ProductListRepository()

def make_get_products_usecase() -> usecases.GetProductsUsecase:
    return usecases.GetProductsUsecase(
        product_repo=make_product_list_repository(),
    )

def make_create_product_usecase() -> usecases.CreateProductUsecase:
    return usecases.CreateProductUsecase(
        product_repo=make_product_list_repository(),
    )
