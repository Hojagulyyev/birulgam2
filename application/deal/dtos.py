from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal

from core.errors import InvalidError
from domain.deal.entities import Deal


@dataclass
class GetDealsUsecaseDto:
    company_id: int
    ids: list[int] | None = None
    type: str | None = None
    first: int | None = None
    skip: int | None = None
    order_by: str | None = None


@dataclass
class CreateDealUsecaseDto:
    company_id: int
    store_id: int
    created_by_id: int
    seller_id: int | None
    buyer_id: int | None

    total_amount: Decimal
    type: str
    created_at: datetime

    installments_total_amount: int = 0
    installments: int = 0
    installment_amount: int = 0
    installment_trifle: int = 0
    installment_expiration_date: date | None = None
    last_paid_at: datetime | None = None
    closed_at: datetime | None = None
    note: str | None = None

    def validate(self):
        if self.total_amount < self.installments_total_amount:
            raise InvalidError(
                loc=['input', 'installments_total_amount'], 
                msg='installments total amount must be less than total amount',
            )
