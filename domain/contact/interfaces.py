from abc import ABC, abstractmethod

from .entities import Contact


class IContactRepository(ABC):

    @abstractmethod
    async def list(self):
        raise NotImplementedError
    
    @abstractmethod
    async def save(self, contact: Contact):
        raise NotImplementedError
    
    # @abstractmethod
    # async def delete(self, id: int):
    #     raise NotImplementedError
