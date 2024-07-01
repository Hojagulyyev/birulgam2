# type: ignore

from enum import Enum, auto


class EnumAutoName(str, Enum):
    def _generate_next_value_(name, start, count, last_values) -> str:
        return name


__all__ = [
    'EnumAutoName',
    'auto',
]
