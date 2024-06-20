from datetime import datetime

from core.errors import (
    DoesNotExistError, 
    InvalidError,
)
from domain.payment.entities import Payment
from domain.payment.interfaces import IPaymentRepository
from domain.deal.interfaces import IDealRepository
from domain.store.interfaces import IStoreRepository

from .dtos import (
    CreatePaymentUsecaseDto,
)


class CreatePaymentUsecase:

    def __init__(
        self, 
        payment_repo: IPaymentRepository,
        deal_repo: IDealRepository,
        store_repo: IStoreRepository,
    ):
        self.payment_repo = payment_repo
        self.deal_repo = deal_repo
        self.store_repo = store_repo
    
    async def execute(self, dto: CreatePaymentUsecaseDto) -> Payment:
        # >>> SECURITY
        deal = await self.deal_repo.get_by_id(
            company_id=dto.company_id,
            id=dto.deal_id,
        )
        if not deal:
            raise DoesNotExistError(loc=['input', 'deal_id'])
        
        # >>> VALIDATION
        if dto.amount > deal.remaining_amount_due:
            raise InvalidError(
                'amount must not be greater than '
                'deal remaining amount due',
                loc=['amount'],
            )
        
        if dto.created_at < deal.created_at:
            raise InvalidError(
                'created_at must be greater than deal created_at',
                loc=['created_at'],
            )

        # >>> MAIN
        payment = Payment(
            id=0,
            company_id=dto.company_id,
            store_id=deal.store_id,
            user_id=dto.user_id,
            deal_id=dto.deal_id,
            sender_id=dto.sender_id,
            receiver_id=dto.receiver_id,

            amount=dto.amount,
            type=dto.type,
            method=dto.method,
            category=dto.category,

            created_at=dto.created_at,
        )
        payment.validate()
        created_payment = await self.payment_repo.save(payment)

        # >>> SIDE EFFECT
        deal.remaining_amount_due -= payment.amount
        deal.last_paid_at = datetime.now()

        if deal.remaining_amount_due == 0:
            deal.closed_at = datetime.now()

        if (
            deal.installments_total_amount
            and deal.remaining_amount_due < deal.installments_total_amount
        ):
            deal.update_installment_expiration_date()

        deal.validate()
        await self.deal_repo.save(deal)

        # >>> RESPONSE
        if 'deal' in dto.selected_fields:
            created_payment.deal = deal
        return created_payment
