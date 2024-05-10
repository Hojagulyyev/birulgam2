from strawberry.types import Info

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
