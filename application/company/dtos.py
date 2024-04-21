from dataclasses import dataclass

from core.random import generate_random_string


@dataclass
class CreateCompanyUsecaseDto:
    name: str | None = None

    def __post_init__(self):
        if self.name is None:
            self.name = generate_random_string()
