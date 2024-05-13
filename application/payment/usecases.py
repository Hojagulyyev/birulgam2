from domain.payment.entities import Payment
from domain.payment.interfaces import IPaymentRepository
from domain.deal.entities import Deal
from domain.deal.interfaces import IDealRepository

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
        payment = Payment(
            id=None,
            company_id=dto.company_id,
            store_id=dto.store_id,
            user_id=dto.user_id,
            deal_id=dto.deal_id,
            prayer_id=dto.prayer_id,
            receiver_id=dto.receiver_id,

            amount=dto.amount,
            type=dto.type,
            method=dto.method,
            category=dto.category,

            created_at=dto.created_at,
        )
        payment.validate()

        created_payment = await self.payment_repo.save(payment)
        return created_payment
