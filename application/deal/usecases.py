from core.errors import DoesNotExistError
from domain.deal.entities import Deal, DealsConnection
from domain.deal.interfaces import IDealRepository
from domain.store.interfaces import IStoreRepository

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

    async def execute(self, dto: GetDealsUsecaseDto) -> DealsConnection:
        deals_connection = await (
            self.deal_repo
            .list(
                ids=dto.ids, 
                company_id=dto.company_id,
                limit=dto.limit,
                offset=dto.offset,
                order_by=dto.order_by,
            )
        )
        return deals_connection


class CreateDealUsecase:

    def __init__(
        self, 
        deal_repo: IDealRepository,
        store_repo: IStoreRepository,
    ):
        self.deal_repo = deal_repo
        self.store_repo = store_repo
    
    async def execute(self, dto: CreateDealUsecaseDto) -> Deal:
        # >>> SECURITY
        store = await self.store_repo.get_by_id(
            company_id=dto.company_id,
            id=dto.store_id,
        )
        if not store:
            raise DoesNotExistError(loc=['input', 'store_id'])
        
        # >>> VALIDATION
        dto.validate()

        # >>> MAIN
        deal = Deal(
            id=0,
            company_id=dto.company_id,
            store_id=dto.store_id,
            user_id=dto.user_id,
            seller_id=dto.seller_id,
            buyer_id=dto.buyer_id,
            store_code=store.code,
            code_number=0,
            total_amount=dto.total_amount,
            remaining_amount_due=dto.total_amount,
            type=dto.type,
            installments_total_amount=dto.installments_total_amount,
            installments=dto.installments,
            installment_amount=dto.installment_amount,
            installment_trifle=dto.installment_trifle,
            installment_expiration_date=dto.installment_expiration_date,
            created_at=dto.created_at,
            last_paid_at=dto.last_paid_at,
            closed_at=dto.closed_at,
            note=dto.note,
        )
        if deal.installments_total_amount:
            deal.update_installment_expiration_date()

        deal.validate()
        created_deal = await self.deal_repo.save(deal)

        # >>> RESPONSE
        return created_deal
