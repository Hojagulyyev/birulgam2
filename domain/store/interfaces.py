from abc import ABC, abstractmethod

from .entities import Store


class IStoreRepository(ABC):
    
    @abstractmethod
    async def save(self, store: Store) -> Store:
        raise NotImplementedError
