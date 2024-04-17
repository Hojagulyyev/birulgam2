from abc import ABC, abstractmethod


class IProductRepository(ABC):

    @abstractmethod
    def list(self):
        raise NotImplementedError
    
    @abstractmethod
    def save(self):
        raise NotImplementedError
