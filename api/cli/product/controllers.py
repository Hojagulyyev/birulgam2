from application.product import dtos

from adapters.product import factory


def get_products_controller():    
    create_product_usecase = factory.make_get_products_usecase()
    products = create_product_usecase.execute(
        dtos.GetProductsUsecaseDto(),
    )
    return products


def create_product_controller():
    name = input("name: ")

    create_product_usecase = factory.make_create_product_usecase()
    product = create_product_usecase.execute(
        dtos.CreateProductUsecaseDto(name=name),
    )
    return product
