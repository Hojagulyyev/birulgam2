from asyncpg import create_pool


DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/birulgam2"

# TODO: close connection
async def get_pool():
    pool = await create_pool(DATABASE_URL)
    return pool
