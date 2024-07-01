from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class CreatePaymentUsecaseDto:
    selected_fields: dict
    company_id: int
    user_id: int
    deal_id: int
    sender_id: int | None
    receiver_id: int | None
    amount: Decimal
    method: str
    created_at: datetime
