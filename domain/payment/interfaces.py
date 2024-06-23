from abc import ABC, abstractmethod

from .entities import Payment, PaymentsConnection


class IPaymentRepository(ABC):

    @abstractmethod
    async def list(
        self,
        ids: list[int] | None = None,
        company_id: int | None = None,
    ) -> PaymentsConnection:
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(
        self,
        id: int,
        company_id: int | None = None,
    ) -> Payment | None:
        raise NotImplementedError

    @abstractmethod
    async def save(self, payment: Payment) -> Payment:
        raise NotImplementedError
