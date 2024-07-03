from typing import Annotated
from datetime import datetime

import strawberry
from strawberry.types import Info

from core.errors import Error
from domain.user_session.entities import UserSession

from application.deal.usecases import (
    CreateDealUsecase,
    GetDealsUsecase,
) 
from application.deal.dtos import (
    GetDealsUsecaseDto,
    CreateDealUsecaseDto,
)

from adapters.deal.map import DealMap
from adapters.deal.repositories import DealPgRepository
from adapters.store.repositories import StorePgRepository

from domain.deal.entities import Deal

from ..error.schemas import ErrorSchema
from .schemas import (
    DealSchema, 
    DealsConnectionSchema, 
    DealTypeSchema,
)
from .inputs import (
    CreateDealInput,
)


get_deals_response = Annotated[
    DealsConnectionSchema | ErrorSchema,
    strawberry.union('GetDealsResponse'),
]
async def get_deals_resolver(
    info: Info,
    ids: list[int] | None = None,
    type: DealTypeSchema | None = None,
    first: int | None = None,
    skip: int | None = None,
    order_by: str | None = None,
) -> get_deals_response:
    user_session: UserSession = info.context["user_session"]
    try:
        company_id: int = user_session.company_id

        async with info.context["pgpool"].acquire() as conn:
            get_deals_usecase = GetDealsUsecase(
                DealPgRepository(conn=conn),
            )
            deals_connection = await get_deals_usecase.execute(
                dto=GetDealsUsecaseDto(
                    company_id=company_id,
                    ids=ids,
                    type=type.value if type else None,
                    first=first,
                    skip=skip,
                    order_by=order_by,
                )
            )
    except Error as e:
        return ErrorSchema(**e.serialize())
    
    deal_schema_list = [
        DealMap.to_gql_schema(deal)
        for deal in deals_connection.nodes
    ]
    response = DealsConnectionSchema(
        nodes=deal_schema_list,
        count=deals_connection.count,
        total=deals_connection.total,
    )
    return response


create_deal_response = Annotated[
    DealSchema | ErrorSchema,
    strawberry.union('CreateDealResponse'),
]
async def create_deal_resolver(
    info: Info,
    input: CreateDealInput,
) -> create_deal_response:
    user_session: UserSession = info.context["user_session"]
    try:
        async with info.context["pgpool"].acquire() as conn:
            user_id: int = user_session.user_id
            company_id: int = user_session.company_id

            create_deal_usecase = CreateDealUsecase(
                deal_repo=DealPgRepository(conn),
                store_repo=StorePgRepository(conn),
            )
            deal = await create_deal_usecase.execute(
                CreateDealUsecaseDto(
                    company_id=company_id,
                    store_id=input.store_id,
                    created_by_id=user_id,
                    seller_id=input.seller_id,
                    buyer_id=input.buyer_id,
                    total_amount=input.total_amount,
                    type=input.type.value,
                    installments_total_amount=input.installments_total_amount,
                    installments=input.installments,
                    installment_amount=input.installment_amount,
                    installment_trifle=input.installment_trifle,
                    installment_expiration_date=input.installment_expiration_date,
                    created_at=input.created_at or datetime.now(),
                    last_paid_at=input.last_paid_at,
                    closed_at=input.closed_at,
                    note=input.note,
                ),
            )
    except Error as e:
        return ErrorSchema(**e.serialize())
        
    response = DealMap.to_gql_schema(deal)
    return response
