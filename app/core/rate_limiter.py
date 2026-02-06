import time
from fastapi import HTTPException, Request
from app.core.cache import redis_client

RATE_LIMIT = 10  # requests
WINDOW = 60      # seconds

def rate_limit(request: Request):
    ip = request.client.host
    key = f"rate:{ip}"
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
