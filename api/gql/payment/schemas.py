from datetime import datetime
from decimal import Decimal

import strawberry

from core.enum import *

from ..company.schemas import CompanySchema
from ..store.schemas import StoreSchema
from ..user.schemas import UserSchema
from ..deal.schemas import DealSchema, DealTypeSchema
from ..contact.schemas import ContactSchema
 

@strawberry.enum
class PaymentTypeSchema(EnumAutoName):
    INCOME = auto()
    EXPENSE = auto()


@strawberry.enum
class PaymentMethodSchema(EnumAutoName):
    CASH = auto()
    ONLINE = auto()

 
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
    type: PaymentTypeSchema
    method: PaymentMethodSchema
    category: DealTypeSchema
    created_at: datetime

    company: CompanySchema | None = None
    store: StoreSchema | None = None
    user: UserSchema | None = None
    deal: DealSchema | None = None
    sender: ContactSchema | None = None
    receiver: ContactSchema | None = None


@strawberry.type
class PaymentsConnectionSchema:
    payments: list[PaymentSchema]
    total: int
