from datetime import datetime
from decimal import Decimal

import strawberry


@strawberry.input
class CreatePaymentInput:
    deal_id: int
    sender_id: int | None = None
    receiver_id: int | None = None
    amount: Decimal
    method: str
    created_at: datetime | None = None
