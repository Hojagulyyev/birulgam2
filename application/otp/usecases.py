from core.random import generate_otp

from adapters.otp.repositories import OtpRedisRepository

from .dtos import SendOtpUsecaseDto


class SendOtpUsecase:

    def __init__(self):
        pass

    async def execute(
        self, 
        dto: SendOtpUsecaseDto,
    ) -> str:
        dto.validate()
        otp = generate_otp()
        otp_repo = OtpRedisRepository()
        otp_repo.set_by_phone(dto.phone, otp)
        # otp_service.send_otp(otp) implement this service
        print('otp', otp)
        return dto.phone
