from asyncpg import create_pool

from infrastructure import env


DATABASE_URL = (
    f"{env.DB_SCHEMA}://"
    f"{env.DB_USER}:{env.DB_USER_PASSWORD}"
    f"@{env.DB_HOST}:{env.DB_PORT}"
    f"/{env.DB_NAME}"
)

class Database():

    async def create_pool(self):
        self.pool = await create_pool(dsn=DATABASE_URL)
    

db = Database()