from dataclasses import dataclass


@dataclass
class CreateCompanyUsecaseDto:
    user_id: int
    access_token: str
    name: str
