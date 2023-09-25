from settings import settings
from redis import Redis


redis = Redis(host=settings.DATABASE.REDIS_HOST, port=settings.DATABASE.REDIS_PORT)
print(redis.ping())
