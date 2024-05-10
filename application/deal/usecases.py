from domain.deal.entities import Deal, DealPage
from domain.deal.interfaces import IDealRepository


class GetDealsUsecase:

    def __init__(
        self, 
        deal_repo: IDealRepository,
    ):
        self.deal_repo = deal_repo

    async def execute(self) -> DealPage:
        deal_page = await self.deal_repo.list()
        return deal_page
