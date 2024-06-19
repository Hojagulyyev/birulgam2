from datetime import date, datetime
from decimal import Decimal

import strawberry

from ..company.schemas import CompanySchema
from ..store.schemas import StoreSchema
from ..user.schemas import UserSchema
from ..contact.schemas import ContactSchema
 
 
@strawberry.type
class DealSchema:
    id: int
    company_id: int
    store_id: int
    user_id: int
    seller_id: int | None
    buyer_id: int | None

    code: str
    total_amount: Decimal
    remaining_amount_due: Decimal
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

    company: CompanySchema | None = None
    store: StoreSchema | None = None
    user: UserSchema | None = None
    seller: ContactSchema | None = None
    buyer: ContactSchema | None = None


@strawberry.type
class DealPageSchema:
    deals: list[DealSchema]
    total: int
