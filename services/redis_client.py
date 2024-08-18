import redis
from config import Config


class RedisDB:
    def __init__(self, uri: str = Config.REDIS_URI):
        self.redis_client = redis.from_url(uri)

    def get(self, key):
        return self.redis_client.get(key)

    def get_with_prefix(self, key, prefix: str):
        return self.redis_client.get(f"{prefix}|{key}")

    def set(self, key, value):
        self.redis_client.set(key, value)

    def set_with_prefix(self, key, value, prefix: str):
        self.redis_client.set(f"{prefix}|{key}", value)


redis_db = RedisDB()
