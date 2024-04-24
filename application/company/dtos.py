from dataclasses import dataclass

from core.random import generate_random_string


@dataclass
class CreateCompanyUsecaseDto:
    name: str = generate_random_string()
