from domain.deal.entities import Deal, DealPage
from domain.deal.interfaces import IDealRepository

from .dtos import (
    GetDealsUsecaseDto,
    CreateDealUsecaseDto,
)


class GetDealsUsecase:

    def __init__(
        self, 
        deal_repo: IDealRepository,
    ):
        self.deal_repo = deal_repo

    async def execute(self, dto: GetDealsUsecaseDto) -> DealPage:
        deal_page = await (
            self.deal_repo
            .list(company_id=dto.company_id)
        )
        return deal_page


class CreateDealUsecase:

    def __init__(
        self, 
        deal_repo: IDealRepository,
    ):
        self.deal_repo = deal_repo
    
    async def execute(self, dto: CreateDealUsecaseDto) -> Deal:
        deal = Deal(
            id=None,
            company_id=dto.company_id,
            store_id=dto.store_id,
            user_id=dto.user_id,
            seller_id=dto.seller_id,
            buyer_id=dto.buyer_id,
            total_amount=dto.total_amount,
            remaining_amount_due=dto.remaining_amount_due,
            type=dto.type,
            installments=dto.installments,
            installment_amount=dto.installment_amount,
            installment_trifle=dto.installment_trifle,
            installment_expiration_date=dto.installment_expiration_date,
            created_at=dto.created_at,
            last_paid_at=dto.last_paid_at,
            closed_at=dto.closed_at,
            note=dto.note,
        )
        deal.validate()
        created_deal = await self.deal_repo.save(deal)
        return created_deal
