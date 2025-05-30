import redis


def get_redis_connection() -> redis.Redis:
    connection = redis.Redis(
        host='localhost',
        port=6379,
        db=0
    )
    return connection



