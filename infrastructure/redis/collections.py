from enum import Enum

class RedisCollection(str, Enum):
    ACCESS_TOKENS = "access_tokens"
    REFRESH_TOKENS = "refresh_tokens"
