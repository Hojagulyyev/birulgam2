import redis

from infrastructure import env


cache = redis.StrictRedis(
    host=env.REDIS_HOST,
    port=env.REDIS_PORT,
    password=env.REDIS_PASSWORD,
    db=env.REDIS_INDEX,
    decode_responses=True,
)
