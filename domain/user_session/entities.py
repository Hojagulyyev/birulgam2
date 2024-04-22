from dataclasses import dataclass


@dataclass
class UserSession:
    user_id: int
    company_id: int

    def __post_init__(self):
        if not isinstance(self.user_id, int):
            raise TypeError
        if not isinstance(self.company_id, int):
            raise TypeError
