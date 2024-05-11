from abc import ABC, abstractmethod

from .entities import Payment


class IPaymentRepository(ABC):

    @abstractmethod
    async def save(self, payment: Payment) -> Payment:
        raise NotImplementedError
    