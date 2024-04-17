from fastapi import (
    APIRouter,
    Depends,
    status,
)

from application.product.usecases import (
    GetProductsUsecase,
    CreateProductUsecase,
) 
from application.product.dtos import (
    GetProductsUsecaseDto,
    CreateProductUsecaseDto,
)
from adapters.product.repositories import ProductSqliteRepository
from adapters.product.map import ProductMap
from infrastructure.sqlite3 import get_conn

from .dtos import (
    GetProductsControllerDto,
    CreateProductControllerDto,
)


router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
)
def get_products_controller(
    dto: GetProductsControllerDto = Depends(),
):
    with get_conn() as conn:
        product_repo = ProductSqliteRepository(conn=conn)
        get_products_usecase = GetProductsUsecase(
            product_repo=product_repo,
        )
        products = get_products_usecase.execute(GetProductsUsecaseDto())
    
    response = ProductMap.serialize_many(products)
    return response


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
)
def create_product_controller(
    dto: CreateProductControllerDto,
):
    with get_conn() as conn:
        product_repo = ProductSqliteRepository(conn=conn)
        create_product_usecase = CreateProductUsecase(
            product_repo=product_repo,
        )
        product = create_product_usecase.execute(
            CreateProductUsecaseDto(name=dto.name),
        )
    
    response = ProductMap.serialize_one(product)
    return response
