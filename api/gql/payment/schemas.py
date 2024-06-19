from datetime import datetime
from decimal import Decimal

import strawberry

from ..company.schemas import CompanySchema
from ..store.schemas import StoreSchema
from ..user.schemas import UserSchema
from ..deal.schemas import DealSchema
from ..contact.schemas import ContactSchema
 
 
@strawberry.type
class PaymentSchema:
    id: int | None
    company_id: int
    store_id: int
    user_id: int
    deal_id: int
    sender_id: int | None
    receiver_id: int | None

    amount: Decimal
    type: str
    method: str
    category: str

    created_at: datetime = datetime.now()

    company: CompanySchema | None = None
    store: StoreSchema | None = None
    user: UserSchema | None = None
    deal: DealSchema | None = None
    sender: ContactSchema | None = None
    receiver: ContactSchema | None = None


@strawberry.type
class PaymentPageSchema:
    payments: list[PaymentSchema]
    total: int
