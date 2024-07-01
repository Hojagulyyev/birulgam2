from datetime import datetime
from decimal import Decimal

import strawberry

from .schemas import PaymentMethodSchema


@strawberry.input
class CreatePaymentInput:
    deal_id: int
    sender_id: int | None = None
    receiver_id: int | None = None
    amount: Decimal
    method: PaymentMethodSchema
    created_at: datetime | None = None
