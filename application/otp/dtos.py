from dataclasses import dataclass

from core.phone import is_valid_phone, format_phone
from core.errors import InvalidError


@dataclass
class SendOtpUsecaseDto:
    phone: str

    def validate(self):
        phone = format_phone(self.phone)
        if not is_valid_phone(phone):
            raise InvalidError(
                loc=['input', 'phone'], 
            )
        return phone
