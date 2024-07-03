from typing import Annotated

import strawberry

from ..error.schemas import ErrorSchema
from .schemas import (
    DealSchema, 
    DealsConnectionSchema,
)


get_deals_response = Annotated[
    DealsConnectionSchema | ErrorSchema,
    strawberry.union('GetDealsResponse'),
]


create_deal_response = Annotated[
    DealSchema | ErrorSchema,
    strawberry.union('CreateDealResponse'),
]