from abc import ABC, abstractmethod

from .entities import Deal, DealPage


class IDealRepository(ABC):

    @abstractmethod
    async def list(
        self,
        company_id: int | None,
    ) -> DealPage:
        raise NotImplementedError

    @abstractmethod
    async def save(self, deal: Deal) -> Deal:
        raise NotImplementedError
    