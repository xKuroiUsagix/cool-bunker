import json
from functools import wraps
from typing import Callable


def cache_response(key_prefix: str, expire: int = 300):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            redis = kwargs.get("redis")
            if not redis:
                return await func(*args, **kwargs)

            cache_key = f"{key_prefix}:{str(args)}:{str(kwargs)}"

            cached = await redis.get(cache_key)
            if cached:
                return json.loads(cached)

            result = await func(*args, **kwargs)

            await redis.set(cache_key, json.dumps(result), ex=expire)
            return result

        return wrapper

    return decorator
