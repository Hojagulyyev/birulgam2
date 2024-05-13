from datetime import datetime
from typing import Literal

import strawberry

from domain.payment.entities import Payment


@strawberry.input
class CreatePaymentInput:
    store_id: int
    deal_id: int
    sender_id: int | None = None
    receiver_id: int | None = None

    amount: int
    type: str
    method: str
    category: str

    created_at: datetime = datetime.now()
