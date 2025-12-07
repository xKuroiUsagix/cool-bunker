import redis.asyncio as aioredis
from app.config import get_settings


settings = get_settings()


class RedisClient:
    def __init__(self):
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
            password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
            encoding="utf-8",
            decode_responses=True,
        )

    async def close(self):
        if self.redis:
            await self.redis.close()

    async def get(self, key: str):
        return await self.redis.get(key)

    async def set(self, key: str, value: str, ex: int = None):
        return await self.redis.set(key, value, ex=ex)

    async def delete(self, key: str):
        return await self.redis.delete(key)


redis_client = RedisClient()


async def get_redis():
    return redis_client.redis
