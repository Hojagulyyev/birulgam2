from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from domain.payment.entities import Payment
from domain.deal.entities import Deal


@dataclass
class CreatePaymentUsecaseDto:
    selected_fields: dict
    company_id: int
    user_id: int
    deal_id: int
    sender_id: int | None
    receiver_id: int | None
    amount: Decimal
    method: Payment.Method
    created_at: datetime = datetime.now()
