from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from dataclasses import dataclass
from enum import Enum, unique
from decimal import Decimal

from core.errors import InvalidError
from domain.company.entities import Company
from domain.store.entities import Store
from domain.user.entities import User
from domain.contact.entities import Contact


@dataclass
class Deal:
    # >>> RELATED
    id: int
    company_id: int
    store_id: int
    user_id: int
    seller_id: int | None
    buyer_id: int | None
    # >>> REQUIRED
    total_amount: Decimal
    remaining_amount_due: Decimal
    type: str
    # >>> OPTIONAL
    code: str | None = None
    installments_total_amount: int = 0
    installments: int = 0
    installment_amount: int = 0
    installment_trifle: int = 0
    installment_expiration_date: date | None = None
    created_at: datetime = datetime.now()
    last_paid_at: datetime | None = None
    closed_at: datetime | None = None
    note: str | None = None
    # >>> MAP
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
        if not isinstance(self.total_amount, Decimal):
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
        if self.installments_total_amount:
            self._validate_installments()
        if self.note:
            self._validate_note()

    def update_installment_expiration_date(self):
        if self.remaining_amount_due == 0:
            self.installment_expiration_date = None
            return
        
        paid_amount = self.installments_total_amount - self.remaining_amount_due
        
        if paid_amount <= self.installment_trifle:
            next_month = 1
            self.installment_expiration_date = (
                self.created_at + relativedelta(months=next_month)
            ).date()
            return
        
        paid_amount_without_trifle = paid_amount - self.installment_trifle
        diff_in_months = int(paid_amount_without_trifle / self.installment_amount)
        next_month_from_month_diff = diff_in_months + 1
        self.installment_expiration_date = (
            self.created_at + relativedelta(months=next_month_from_month_diff)
        ).date()

    def _validate_remaining_amount_due(self):
        if not isinstance(self.remaining_amount_due, Decimal):
            raise TypeError
        
        if self.remaining_amount_due < 0:
            raise InvalidError('deal remaining amount must be a whole number')
        
        if self.remaining_amount_due > self.total_amount:
            raise InvalidError(
                'deal remaining amount must not be greater than total amount')
        
    def _validate_note(self):
        if not isinstance(self.note, str):
            raise TypeError
        
        note_len = len(self.note)
        if note_len > self.NOTE_MAX_LENGTH:
            raise InvalidError(
                f'deal note\'s length must be less than {self.NOTE_MAX_LENGTH}'
            )
        
    def _validate_type(self):
        if self.type not in self.Type.__members__.values():
            raise InvalidError(f'deal type {self.type} does not allowed')
        
    def _validate_installments(self):
        calculated_total_amount = (
            self.installment_amount * 
            self.installments + 
            self.installment_trifle
        )
        if calculated_total_amount != self.installments_total_amount:
            raise InvalidError('deal installments data is inconsistent')


@dataclass
class DealPage:
    deals: list[Deal]
    total: int
