from infrastructure import env
from infrastructure.redis import cache


class OtpRedisRepository:

    def get_by_phone(self, phone: str) -> str | None:
        otp = cache.get(f"otp{phone}")
        if not otp:
            return None
        return str(otp)
        
    def set_by_phone(self, phone: str, otp: str) -> str:
        cache.set(
            f"otp{phone}",
            otp,
            ex=env.OTP_TTL,
        )
        return otp
