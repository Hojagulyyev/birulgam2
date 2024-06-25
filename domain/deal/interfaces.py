from abc import ABC, abstractmethod

from .entities import Deal, DealsConnection


class IDealRepository(ABC):

    @abstractmethod
    async def list(
        self,
        company_id: int | None = None,
        ids: list[int] | None = None,
        first: int | None = None,
        skip: int | None = None,
        order_by: str | None = None,
    ) -> DealsConnection:
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(
        self,
        id: int,
        company_id: int | None = None,
    ) -> Deal | None:
        raise NotImplementedError

    @abstractmethod
    async def save(self, deal: Deal) -> Deal:
        raise NotImplementedError
    