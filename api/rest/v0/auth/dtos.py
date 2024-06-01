from pydantic import BaseModel, Field, field_validator
from fastapi import HTTPException, status

from core.phone import is_valid_phone, format_phone
from domain.user.entities import User


OTP_LENGTH = 5


class SignupControllerDto(BaseModel):
    username: str = Field(
        ...,
        min_length=User.USERNAME_MIN_LENGTH,
        max_length=User.USERNAME_MAX_LENGTH,
    )
    password: str = Field(
        ...,
        min_length=User.PASSWORD_MIN_LENGTH,
    )
    password_confirm: str = Field(
        ...,
        min_length=User.PASSWORD_MIN_LENGTH,
    )
    create_company: bool = False


class SigninControllerDto(BaseModel):
    username: str = Field(
        ...,
        min_length=User.USERNAME_MIN_LENGTH,
        max_length=User.USERNAME_MAX_LENGTH,
    )
    password: str = Field(
        ...,
        min_length=User.PASSWORD_MIN_LENGTH,
    )


class SendOtpControllerDto(BaseModel):
    phone: str

    @field_validator('phone')
    def validate_phone(cls, phone):
        phone = format_phone(phone)
        if not is_valid_phone(phone):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="invalid phone",
            )
        return phone


class SigninByOtpControllerDto(BaseModel):
    phone: str = Field(
        ...,
        min_length=User.USERNAME_MIN_LENGTH,
        max_length=User.USERNAME_MAX_LENGTH,
    )
    otp: str = Field(
        ...,
        min_length=OTP_LENGTH,
        max_length=OTP_LENGTH,
    )

    @field_validator('phone')
    def validate_phone(cls, phone):
        phone = format_phone(phone)
        if not is_valid_phone(phone):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="invalid phone",
            )
        return phone
