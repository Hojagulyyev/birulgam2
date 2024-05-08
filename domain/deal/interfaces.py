from abc import ABC, abstractmethod

from .entities import Deal


class IDealRepository(ABC):

    @abstractmethod
    async def save(self, deal: Deal) -> Deal:
        raise NotImplementedError
    