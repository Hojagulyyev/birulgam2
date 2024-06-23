from abc import ABC, abstractmethod

from .entities import Contact, ContactsConnection


class IContactRepository(ABC):

    @abstractmethod
    async def list(
        self, 
        company_id: int | None,
        limit: int | None = None,
        offset: int | None = None,
        order_by: str | None = None,
    ) -> ContactsConnection:
        raise NotImplementedError
    
    @abstractmethod
    async def save(self, contact: Contact):
        raise NotImplementedError
    
    # @abstractmethod
    # async def delete(self, id: int):
    #     raise NotImplementedError
