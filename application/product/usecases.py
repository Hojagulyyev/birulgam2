from domain.product.entities import Product
from domain.product.interfaces import IProductRepository

from . import dtos


class GetProductsUsecase:

    def __init__(self, product_repo: IProductRepository):
        self.product_repo = product_repo

    def execute(self, dto: dtos.GetProductsUsecaseDto) -> list[Product]:
        products = self.product_repo.list()
        return products


class CreateProductUsecase:

    def __init__(self, product_repo: IProductRepository):
        self.product_repo = product_repo

    def execute(self, dto: dtos.CreateProductUsecaseDto) -> Product:
        product = Product(name=dto.name)
        created_product = self.product_repo.save(product)
        return created_product
