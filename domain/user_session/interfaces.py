from abc import ABC, abstractmethod

from .entities import User


class IUserSessionRepository(ABC):

    @abstractmethod
    async def get_by_access_token(self, access_token: str):
        raise NotImplementedError
    
    @abstractmethod
    async def save(self, contact: User):
        raise NotImplementedError
