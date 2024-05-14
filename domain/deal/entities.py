from datetime import datetime, date
from dataclasses import dataclass
from enum import Enum, unique

from domain.company.entities import Company
from domain.store.entities import Store
from domain.user.entities import User
from domain.contact.entities import Contact


@dataclass
class Deal:
    id: int | None
    company_id: int
    store_id: int
    user_id: int
    seller_id: int | None
    buyer_id: int | None

    total_amount: int
    remaining_amount_due: int
    type: str

    installments: int = 0
    installment_amount: int = 0
    installment_trifle: int = 0
    installment_expiration_date: date | None = None
    created_at: datetime = datetime.now()
    last_paid_at: datetime | None = None
    closed_at: datetime | None = None
    note: str | None = None

    company: Company | None = None
    store: Store | None = None
    user: User | None = None
    seller: Contact | None = None
    buyer: Contact | None = None

    @unique
    class Type(str, Enum):
        SALE = "sale"
        PURCHASE = "purchase"

    NOTE_MAX_LENGTH = 255

    def validate(self):
        if not isinstance(self.id, int | None):
            raise TypeError
        if not isinstance(self.company_id, int):
            raise TypeError
        if not isinstance(self.store_id, int):
            raise TypeError
        if not isinstance(self.user_id, int):
            raise TypeError
        if not isinstance(self.seller_id, int | None):
            raise TypeError
        if not isinstance(self.buyer_id, int | None):
            raise TypeError
        if not isinstance(self.total_amount, int):
            raise TypeError
        if not isinstance(self.installments, int):
            raise TypeError
        if not isinstance(self.installment_amount, int):
            raise TypeError
        if not isinstance(self.installment_trifle, int):
            raise TypeError
        if not isinstance(self.installment_expiration_date, date | None):
            raise TypeError
        if not isinstance(self.created_at, datetime):
            raise TypeError
        if not isinstance(self.last_paid_at, datetime | None):
            raise TypeError
        if not isinstance(self.closed_at, datetime | None):
            raise TypeError
            
        self._validate_remaining_amount_due()
        self._validate_type()
        if self.note:
            self._validate_note()

    def _validate_remaining_amount_due(self):
        if not isinstance(self.remaining_amount_due, int):
            raise TypeError
        
        if self.remaining_amount_due < 0:
            raise ValueError('deal remaining amount must be a whole number')
        
        if self.remaining_amount_due > self.total_amount:
            raise ValueError('deal remaining amount must not be greater than total amount')
        
    def _validate_note(self):
        if not isinstance(self.note, str):
            raise TypeError
        
        note_len = len(self.note)
        if note_len > self.NOTE_MAX_LENGTH:
            raise ValueError(f'deal note\'s length must be less than {self.NOTE_MAX_LENGTH}')
        
    def _validate_type(self):
        if self.type not in self.Type.__members__.values():
            raise ValueError(f'deal type {self.type} does not allowed')
        
    def _validate_installments(self):
        calculated_total_amount = (
            self.installment_amount * 
            self.installments + 
            self.installment_trifle
        )
        if calculated_total_amount != self.total_amount:
            raise ValueError('deal installments data is inconsistent')


@dataclass
class DealPage:
    deals: list[Deal]
    total: int
