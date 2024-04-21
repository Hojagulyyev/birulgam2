from dataclasses import dataclass


@dataclass
class CreateUserUsecaseDto:
    username: str
    password: str
    company_id: int
