from asyncpg import create_pool


DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/birulgam2"


class Database():

    async def create_pool(self):
        self.pool = await create_pool(dsn=DATABASE_URL)
    