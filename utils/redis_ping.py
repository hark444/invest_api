from settings import settings
from redis import Redis


redis = Redis(host=settings.DATABASE.REDIS_HOST, port=settings.DATABASE.REDIS_PORT, db=2)
print(redis.ping())
