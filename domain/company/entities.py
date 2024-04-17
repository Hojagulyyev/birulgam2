from dataclasses import dataclass


@dataclass
class Company:
    NAME_MIN_LENGTH = 3
    NAME_MAX_LENGTH = 16

    id: int | None = None
    name: str


    def __post_init__(self):
        if not isinstance(self.id, int | None):
            raise TypeError
        self._validate_name()
        
        
    def _validate_name(self):
        if not isinstance(self.name, str):
            raise TypeError
        if (
            self.name < self.NAME_MIN_LENGTH
            or self.name > self.NAME_MAX_LENGTH
        ):
            raise ValueError('company name\'s length must be between {NAME_MIN_LENGTH} and {NAME_MAX_LENGTH}')
