import redis

from settings import Settings


def get_redis_connection() -> redis.Redis:
    settings = Settings()
    connection = redis.Redis(
        host=settings.CACHE_HOST,
        port=settings.CACHE_PORT,
        db=settings.CACHE_NAME
    )
    return connection



