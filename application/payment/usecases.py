from datetime import datetime

from domain.payment.entities import Payment
from domain.payment.interfaces import IPaymentRepository
from domain.deal.entities import Deal
from domain.deal.interfaces import IDealRepository

from application.errors import (
    DoesNotExistError, 
    InvalidError,
)

from .dtos import (
    CreatePaymentUsecaseDto,
)


class CreatePaymentUsecase:

    def __init__(
        self, 
        payment_repo: IPaymentRepository,
        deal_repo: IDealRepository,
    ):
        self.payment_repo = payment_repo
        self.deal_repo = deal_repo
    
    async def execute(self, dto: CreatePaymentUsecaseDto) -> Payment:
        deal = await self.deal_repo.get_by_id(
            company_id=dto.company_id,
            id=dto.deal_id,
        )
        if not deal:
            raise DoesNotExistError(loc=['deal_id'])
        
        if dto.amount > deal.remaining_amount_due:
            raise InvalidError(
                loc=['amount'],
                msg=(
                    'amount must not be greater than '
                    'deal remaining amount due'
                ),
            )

        if dto.created_at < deal.created_at:
            raise InvalidError(
                loc=['created_at'],
                msg='created_at must be greater than deal created_at'
            )

        payment = Payment(
            id=None,
            company_id=dto.company_id,
            store_id=dto.store_id,
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

        deal.remaining_amount_due -= payment.amount
        deal.last_paid_at = datetime.now()

        if deal.remaining_amount_due == 0:
            deal.closed_at = datetime.now()

        deal.validate()
        await self.deal_repo.save(deal)

        return created_payment
