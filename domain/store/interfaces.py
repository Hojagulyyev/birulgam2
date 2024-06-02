from abc import ABC, abstractmethod

from .entities import Store


class IStoreRepository(ABC):
    
    @abstractmethod
    async def get_by_id(self, company_id: int | None, id: int) -> Store | None:
        raise NotImplementedError
    
    @abstractmethod
    async def save(self, store: Store) -> Store:
        raise NotImplementedError
