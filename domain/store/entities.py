from dataclasses import dataclass


@dataclass
class Store:
    company_id: int
    name: str
    code: str
    id: int | None = None

    NAME_MIN_LENGTH = 3
    NAME_MAX_LENGTH = 26
    NAME_RANDOM_LENGTH = 8

    CODE_MIN_LENGTH = 2
    CODE_MAX_LENGTH = 2

    def __post_init__(self):
        if not isinstance(self.id, int | None):
            raise TypeError
        self._validate_name()
        self._validate_code()
        
    def _validate_name(self):
        if not isinstance(self.name, str):
            raise TypeError
        
        name_len = len(self.name)
        if (
            name_len < self.NAME_MIN_LENGTH
            or name_len > self.NAME_MAX_LENGTH
        ):
            raise ValueError(f'store name\'s length must be between {self.NAME_MIN_LENGTH} and {self.NAME_MAX_LENGTH}')

    def _validate_code(self):
        if not isinstance(self.code, str):
            raise TypeError
        
        code_len = len(self.code)
        if (
            code_len < self.CODE_MIN_LENGTH
            or code_len > self.CODE_MAX_LENGTH
        ):
            raise ValueError(f'store code\'s length must be between {self.CODE_MIN_LENGTH} and {self.CODE_MAX_LENGTH}')
