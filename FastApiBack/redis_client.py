# redis_client.py
import ssl

from config import settings
from redis.asyncio import Redis

redis_url = settings.REDIS_URL

if redis_url.startswith("rediss://"):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    redis = Redis.from_url(
        redis_url,
        ssl_context=ssl_context,
        decode_responses=False,
        socket_timeout=5,
        socket_connect_timeout=5,
        retry_on_timeout=True,
        max_connections=10,
    )
else:
    redis = Redis.from_url(
        redis_url,
        decode_responses=False,
        socket_timeout=5,
        socket_connect_timeout=5,
        retry_on_timeout=True,
        max_connections=10,
    )
