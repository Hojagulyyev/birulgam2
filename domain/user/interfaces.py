from abc import ABC, abstractmethod

from .entities import User


class IUserRepository(ABC):

    # @abstractmethod
    # async def list(self):
    #     raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str) -> User:
        raise NotImplementedError
    
    @abstractmethod
    async def join_companies(self, user: User) -> User:
        raise NotImplementedError
    
    @abstractmethod
    async def save(self, user: User) -> User:
        raise NotImplementedError
    
    # @abstractmethod
    # async def delete(self, id: int):
    #     raise NotImplementedError


class IUserPasswordService(ABC):

    @abstractmethod
    def hash_password(self, password: str) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def check_password(
        self, 
        plain_password: str, 
        hashed_password: str,
    ) -> bool:
        raise NotImplementedError
    