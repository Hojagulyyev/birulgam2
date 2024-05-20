from dataclasses import dataclass


@dataclass
class Company:
    id: int
    name: str

    NAME_MIN_LENGTH = 3
    NAME_MAX_LENGTH = 16

    def validate(self):
        if not isinstance(self.id, int):
            raise TypeError
        self._validate_name()
        
        
    def _validate_name(self):
        if not isinstance(self.name, str):
            raise TypeError
        
        name_len = len(self.name)
        if (
            name_len < self.NAME_MIN_LENGTH
            or name_len > self.NAME_MAX_LENGTH
        ):
            raise ValueError(
                f'company name\'s length must be between' 
                f'{self.NAME_MIN_LENGTH} and {self.NAME_MAX_LENGTH}'
            )
