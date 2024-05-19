from dataclasses import dataclass


@dataclass
class UserSession:
    user_id: int
    company_ids: list[int] | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.user_id, int):
            raise TypeError
        if not isinstance(self.company_ids, list | None):
            raise TypeError
