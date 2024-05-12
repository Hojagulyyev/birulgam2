from abc import ABC, abstractmethod

from .entities import Contact, ContactPage


class IContactRepository(ABC):

    @abstractmethod
    async def list(
        self, 
        company_id: int | None,
    ) -> ContactPage:
        raise NotImplementedError
    
    @abstractmethod
    async def save(self, contact: Contact):
        raise NotImplementedError
    
    # @abstractmethod
    # async def delete(self, id: int):
    #     raise NotImplementedError
