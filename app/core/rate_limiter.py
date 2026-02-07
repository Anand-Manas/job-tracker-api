import os
from fastapi import HTTPException, Request
from redis import Redis
from redis.exceptions import RedisError

RATE_LIMIT = 10 
WINDOW = 60     
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

try:
    redis_client = Redis(host=REDIS_HOST, port=6379, decode_responses=True)
    redis_client.ping()
except RedisError:
    redis_client = None  

def rate_limit(request: Request):
    if redis_client is None:
        return

    ip = request.client.host
    key = f"rate:{ip}"

    try:
        current = redis_client.get(key)

        if current and int(current) >= RATE_LIMIT:
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )

        pipe = redis_client.pipeline()
        pipe.incr(key, 1)
        pipe.expire(key, WINDOW)
        pipe.execute()

    except RedisError:
        return
