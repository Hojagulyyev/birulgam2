from abc import ABC, abstractmethod


class ICompanyRepository(ABC):
    
    @abstractmethod
    def save(self):
        raise NotImplementedError
