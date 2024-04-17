from dataclasses import dataclass


@dataclass
class GetProductsUsecaseDto:
    pass


@dataclass
class CreateProductUsecaseDto:
    name: str
