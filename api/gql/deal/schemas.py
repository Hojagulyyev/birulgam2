from datetime import date, datetime

import strawberry

from ..company.schemas import CompanySchema
from ..store.schemas import StoreSchema
from ..user.schemas import UserSchema
from ..contact.schemas import ContactSchema
 
 
@strawberry.type
class DealSchema:
    id: int | None
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

    company: CompanySchema | None = None
    store: StoreSchema | None = None
    user: UserSchema | None = None
    seller: ContactSchema | None = None
    buyer: ContactSchema | None = None


@strawberry.type
class DealPageSchema:
    deals: list[DealSchema]
    total: int
