from typing import Annotated

import strawberry
from strawberry.types import Info

from core.errors import Error

from application.otp.usecases import (
    SendOtpUsecase,
    SendOtpUsecaseDto,
)

from ..error.schemas import ErrorSchema
from .schemas import SendOtpResponseSchema
from .inputs import (
    SendOtpInput,
)


send_otp_response = Annotated[
    SendOtpResponseSchema | ErrorSchema,
    strawberry.union('SendOtpResponse'),
]
async def send_otp_resolver(
    info: Info,
    input: SendOtpInput,
) -> send_otp_response:
    try:
        phone = await SendOtpUsecase().execute(
            dto=SendOtpUsecaseDto(input.phone),
        )
    except Error as e:
        return ErrorSchema(**e.serialize())
    
    return SendOtpResponseSchema(phone=phone)
