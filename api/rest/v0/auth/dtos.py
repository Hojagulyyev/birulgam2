from pydantic import BaseModel, Field

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
    phone: str = Field(
        ...,
        min_length=User.USERNAME_MIN_LENGTH,
        max_length=User.USERNAME_MAX_LENGTH,
    )


class SigninByOtpControllerDto(BaseModel):
    phone: str = Field(
        ...,
        min_length=User.USERNAME_MIN_LENGTH,
        max_length=User.USERNAME_MAX_LENGTH,
    )
    otp: str
