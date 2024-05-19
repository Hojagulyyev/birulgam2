from dataclasses import dataclass


@dataclass
class CreateUserSessionUsecaseDto:
    user_id: int
    company_ids: list[int]
