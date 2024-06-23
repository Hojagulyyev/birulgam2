from datetime import date, datetime
from typing import Annotated
from decimal import Decimal

import strawberry


@strawberry.input
class CreateDealInput:
    store_id: int
    
    seller_id: int | None = None
    buyer_id: int | None = None

    total_amount: Decimal
    type: str

    installments_total_amount: int = 0
    installments: Annotated[
        int, strawberry.argument(
            description="The number of installments"
        )] = 0
    installment_amount: Annotated[
        int, strawberry.argument(
            description="The monthly amount of one installment"
        )] = 0
    installment_trifle: int = 0
    installment_expiration_date: date | None = None
    created_at: datetime = datetime.now()
    last_paid_at: datetime | None = None
    closed_at: datetime | None = None
    note: str | None = None
