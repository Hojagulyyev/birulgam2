from core.random import generate_otp
from core.errors import DoesNotExistError

from adapters.otp.repositories import OtpRedisRepository

from .dtos import SendOtpUsecaseDto, ExistOtpUsecaseDto


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


class ExistOtpUsecase:

    def __init__(self):
        pass

    async def execute(
        self, 
        dto: ExistOtpUsecaseDto,
    ) -> bool:
        dto.validate()

        otp_repo = OtpRedisRepository()
        otp = otp_repo.get_by_phone(dto.phone)
        if not otp or otp != dto.otp:
            return False
        otp_repo.remove_by_phone(dto.phone)
        return True
