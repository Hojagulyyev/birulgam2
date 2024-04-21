from fastapi import HTTPException, status
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

    @model_validator(mode="after")
    def validate_passwords(cls, dto):
        if dto.password_confirm != dto.password:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    "password mismatch"
                ),
            )
        return dto
