# from asyncpg import Connection
# from asyncpg.exceptions import UniqueViolationError

# from domain.deal.interfaces import IDealRepository
# from domain.deal.entities import Deal


# class DealPgRepository(IDealRepository):

#     def __init__(self, conn: Connection):
#         self._conn = conn
        
#     async def save(self, deal: Deal) -> Deal:
#         if not deal.id:
#             deal = await self._insert(deal)
#         else:
#             deal = await self._update(deal)
#         return deal
    
#     async def _insert(self, deal: Deal) -> Deal:
#         stmt = (
#             '''
#             INSERT INTO deal
#             (
#                 company_id,
#                 name,
#                 code
#             ) VALUES (
#                 $1, $2, $3
#             )
#             RETURNING id
#             '''
#         )
#         args = (
#             deal.company_id,
#             deal.name,
#             deal.code,
#         )
#         try:
#             inserted_id = await self._conn.fetchval(stmt, *args)
#         except UniqueViolationError as e:
#             raise e

#         deal.id = inserted_id
#         return deal

#     async def _update(self, deal: Deal) -> Deal:
#         stmt = (
#             '''
#             UPDATE deal SET 
#                 company_id = $1,
#                 name = $2,
#                 code = $3
#             WHERE id = $4
#             '''
#         )
#         args = (
#             deal.company_id,
#             deal.name,
#             deal.code,
#             deal.id,
#         )
#         await self._conn.execute(stmt, *args)
#         return deal
