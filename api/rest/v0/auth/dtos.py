from pydantic import BaseModel, Field, model_validator

from domain.user.entities import User


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
