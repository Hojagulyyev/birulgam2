from decouple import config


SECRET = config("SECRET")

DB_SCHEMA = config("DB_SCHEMA")
DB_USER = config("DB_USER")
DB_USER_PASSWORD = config("DB_USER_PASSWORD")
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT")
DB_NAME = config("DB_NAME")

REDIS_HOST = config("REDIS_HOST")
REDIS_PORT = config("REDIS_PORT")
REDIS_PASSWORD = config("REDIS_PASSWORD")
REDIS_INDEX = config("REDIS_INDEX")

ACCESS_TOKEN_EXPIRATION_TIME_IN_SECONDS = config(
    "ACCESS_TOKEN_EXPIRATION_TIME_IN_SECONDS",
    cast=int,
)
