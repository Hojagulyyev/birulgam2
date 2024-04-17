from abc import ABC, abstractmethod


class ICompanyRepository(ABC):
    
    @abstractmethod
    async def save(self):
        raise NotImplementedError
