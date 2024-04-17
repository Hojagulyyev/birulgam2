from typing import Annotated

import strawberry


@strawberry.input
class GetProductsInput:
    search: str | None = None


@strawberry.input
class CreateProductInput:
    name: Annotated[
        str,
        strawberry.argument(description="The product's new name"),
    ]
    price: Annotated[
        float | None,
        strawberry.argument(description="The product's new price"),
    ]
