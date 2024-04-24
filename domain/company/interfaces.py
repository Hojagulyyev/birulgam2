from abc import ABC, abstractmethod

from .entities import Company


class ICompanyRepository(ABC):
    
    @abstractmethod
    async def save(self, company: Company) -> Company:
        raise NotImplementedError
