from dataclasses import dataclass
from datetime import datetime

from domain.deal.entities import Deal


@dataclass
class CreatePaymentUsecaseDto:
    company_id: int
    store_id: int
    user_id: int
    deal_id: int
    prayer_id: int | None
    receiver_id: int | None

    amount: int
    type: str
    method: int
    category: Deal.Type

    created_at: datetime = datetime.now()
