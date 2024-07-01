# type: ignore

from enum import Enum, auto


class EnumAutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


__all__ = [
    'EnumAutoName',
    'auto',
]
