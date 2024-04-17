from dataclasses import dataclass


@dataclass
class Product:
    name: str
    id: int | None = None

    def __post_init__(self):
        if not isinstance(self.id, int | None):
            raise TypeError
        if not isinstance(self.name, str):
            raise TypeError


@dataclass
class Products:
    products: list[Product]
    total: int

    def __post_init__(self):
        if not isinstance(self.total, int):
            raise TypeError
