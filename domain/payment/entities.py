from datetime import datetime, date
from dataclasses import dataclass
from enum import Enum, unique
from decimal import Decimal

from core.errors import InvalidError
from domain.company.entities import Company
from domain.store.entities import Store
from domain.user.entities import User
from domain.contact.entities import Contact
from domain.deal.entities import Deal


@dataclass
class Payment:

    @unique
    class Type(str, Enum):
        INCOME = "income"
        EXPENSE = "expense"

    @unique
    class Method(str, Enum):
        CASH = "cash"
        ONLINE = "online"

    # >>> RELATED
    id: int
    company_id: int
    store_id: int
    user_id: int
    deal_id: int
    sender_id: int | None
    receiver_id: int | None
    # >>> REQUIRED
    amount: Decimal
    type: Type
    method: Method
    category: Deal.Type
    created_at: datetime
    # >>> MAP
    company: Company | None = None
    store: Store | None = None
    user: User | None = None
    deal: Deal | None = None
    sender: Contact | None = None
    receiver: Contact | None = None

    def validate(self):
        if not isinstance(self.id, int | None):
            raise TypeError
        if not isinstance(self.company_id, int):
            raise TypeError
        if not isinstance(self.store_id, int):
            raise TypeError
        if not isinstance(self.user_id, int):
            raise TypeError
        if not isinstance(self.deal_id, int):
            raise TypeError
        if not isinstance(self.sender_id, int | None):
            raise TypeError
        if not isinstance(self.receiver_id, int | None):
            raise TypeError
        if not isinstance(self.amount, Decimal):
            raise TypeError
        if not isinstance(self.created_at, datetime):
            raise TypeError
        
        self._validate_type()
        self._validate_method()
        self._validate_category()
        
    def _validate_type(self):
        if self.type not in self.Type.__members__.values():
            raise InvalidError(f'payment type {self.type} does not allowed')
        
    def _validate_method(self):
        if self.method not in self.Method.__members__.values():
            raise InvalidError(f'payment method {self.method} does not allowed')
        
    def _validate_category(self):
        if self.category not in Deal.Type.__members__.values():
            raise InvalidError(f'payment category {self.category} does not allowed')
    

@dataclass
class PaymentsConnection:
    payments: list[Payment]
    total: int
