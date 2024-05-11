from strawberry.types import Info

from domain.user_session.entities import UserSession

from application.deal.usecases import (
    CreateDealUsecase,
    GetDealsUsecase,
) 
from application.deal.dtos import (
    CreateDealUsecaseDto,
)
from adapters.deal.map import DealMap
from adapters.deal.repositories import DealPgRepository

from .schemas import DealSchema, DealPageSchema
from .inputs import CreateDealInput


async def get_deals_resolver(
    info: Info,
) -> DealPageSchema:
    async with info.context["pgpool"].acquire() as conn:
        get_deals_usecase = GetDealsUsecase(
            DealPgRepository(conn=conn),
        )
        deal_page = await get_deals_usecase.execute()
    
    deal_schema_list = [
        DealMap.to_gql_schema(deal)
        for deal in deal_page.deals
    ]
    response = DealPageSchema(
        deals=deal_schema_list,
        total=deal_page.total,
    )
    return response


async def create_deal_resolver(
    info: Info,
    input: CreateDealInput,
) -> DealSchema:
    user_session: UserSession = info.context["user_session"]

    async with info.context["pgpool"].acquire() as conn:
        create_deal_usecase = CreateDealUsecase(
            deal_repo=DealPgRepository(conn=conn),
        )
        deal = await create_deal_usecase.execute(
            CreateDealUsecaseDto(
                company_id=user_session.company_id,
                store_id=input.store_id,
                user_id=user_session.user_id,
                seller_id=input.seller_id,
                buyer_id=input.buyer_id,

                total_amount=input.total_amount,
                remaining_amount_due=input.remaining_amount_due,
                type=input.type,

                installments=input.installments,
                installment_amount=input.installment_amount,
                installment_trifle=input.installment_trifle,
                installment_expiration_date=input.installment_expiration_date,
                created_at=input.created_at,
                last_paid_at=input.last_paid_at,
                closed_at=input.closed_at,
                note=input.note,
            ),
        )
    response = DealMap.to_gql_schema(deal)
    return response
