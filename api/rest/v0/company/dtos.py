from pydantic import BaseModel, Field

from domain.company.entities import Company


class CreateCompanyControllerDto(BaseModel):
    name: str = Field(
        ...,
        min_length=Company.NAME_MIN_LENGTH,
        max_length=Company.NAME_MAX_LENGTH,
    )
