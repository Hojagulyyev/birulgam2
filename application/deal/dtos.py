from dataclasses import dataclass
from datetime import date, datetime

from core.errors import InvalidError


@dataclass
class GetDealsUsecaseDto:
    company_id: int
    ids: list[int] | None = None


@dataclass
class CreateDealUsecaseDto:
    company_id: int
    store_id: int
    user_id: int
    seller_id: int | None
    buyer_id: int | None

    total_amount: int
    remaining_amount_due: int
    type: str

    installments_total_amount: int = 0
    installments: int = 0
    installment_amount: int = 0
    installment_trifle: int = 0
    installment_expiration_date: date | None = None
    created_at: datetime = datetime.now()
    last_paid_at: datetime | None = None
    closed_at: datetime | None = None
    note: str | None = None

    def validate(self):
        if self.total_amount != self.remaining_amount_due:
            raise InvalidError(
                loc=['input', 'remaining_amount_due'], 
                msg='remaining amount must be equal to total amount',
            )
