from abc import ABC, abstractmethod

from .entities import UserSession


class IUserSessionRepository(ABC):

    @abstractmethod
    async def get_by_access_token(self, access_token: str) -> UserSession:
        raise NotImplementedError
    
    @abstractmethod
    async def set_by_access_token(self, access_token: str, user_session: UserSession) -> UserSession:
        raise NotImplementedError
    
    @abstractmethod
    async def make_empty(self) -> UserSession:
        raise NotImplementedError
