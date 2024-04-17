from pydantic import BaseModel, Field


class GetProductsControllerDto(BaseModel):
    search: str | None = None


class CreateProductControllerDto(BaseModel):
    name: str = Field(min_length=3)
    price: float | None = None
