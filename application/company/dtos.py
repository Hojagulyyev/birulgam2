from dataclasses import dataclass

from core.random import generate_random_string


@dataclass
class CreateCompanyUsecaseDto:
    user_id: int
    access_token: str
    name: str = generate_random_string()
