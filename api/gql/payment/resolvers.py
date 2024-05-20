from typing import Annotated

import strawberry
from strawberry.types import Info

from core.errors import Error
from domain.user_session.entities import UserSession
from domain.payment.entities import Payment
from domain.deal.entities import Deal

from application.payment.usecases import (
    CreatePaymentUsecase,
) 
from application.payment.dtos import (
    CreatePaymentUsecaseDto,
)

from api.gql.utils import get_selected_fields
from adapters.payment.map import PaymentMap
from adapters.payment.repositories import PaymentPgRepository
from adapters.deal.repositories import DealPgRepository

from ..error.schemas import ErrorSchema
from .schemas import PaymentSchema
from .inputs import (
    CreatePaymentInput,
)


create_payment_response = Annotated[
    PaymentSchema | ErrorSchema,
    strawberry.union('CreatePaymentResponse'),
]
async def create_payment_resolver(
    info: Info,
    input: CreatePaymentInput,
) -> create_payment_response:
    user_session: UserSession = info.context["user_session"]
    selected_fields = await get_selected_fields(info)

    async with info.context["pgpool"].acquire() as conn:
        create_payment_usecase = CreatePaymentUsecase(
            payment_repo=PaymentPgRepository(conn=conn),
            deal_repo=DealPgRepository(conn=conn),
        )
        try:
            payment = await create_payment_usecase.execute(
                CreatePaymentUsecaseDto(
                    selected_fields=selected_fields,
                    company_id=user_session.company_id,
                    store_id=input.store_id,
                    user_id=user_session.user_id,
                    deal_id=input.deal_id,
                    sender_id=input.sender_id,
                    receiver_id=input.receiver_id,
                    amount=input.amount,
                    type=Payment.Type(input.type),
                    method=Payment.Method(input.method),
                    category=Deal.Type(input.category),
                    created_at=input.created_at,
                ),
            )
        except Error as e:
            return ErrorSchema(**e.serialize())
        
    response = PaymentMap.to_gql_schema(payment)
    return response
