from abc import ABC, abstractmethod

from .entities import User


class IUserRepository(ABC):

    @abstractmethod
    async def list(self):
        raise NotImplementedError
    
    @abstractmethod
    async def save(self, contact: User):
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, id: int):
        raise NotImplementedError


class IUserPasswordService(ABC):

    @abstractmethod
    async def hash_password(self, password: str):
        raise NotImplementedError
    
    @abstractmethod
    async def check_password(
        self, 
        plain_password: str, 
        hashed_password: str,
    ):
        raise NotImplementedError
    