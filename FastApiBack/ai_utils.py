import json
import logging

from config import settings
from openai import AsyncOpenAI
from redis.asyncio import Redis

# Set the OpenAI API key
client = AsyncOpenAI(
    # This is the default and can be omitted
    api_key=settings.OPENAI_KEY,
)

# Initialize Redis client
redis = Redis(host="localhost", port=6379, db=0, decode_responses=False)


async def get_embedding(text: str, model: str = "text-embedding-3-small") -> list:
    cache_key = f"embedding:{text}"
    # Try to get the embedding from Redis
    try:
        cached_embedding = await redis.get(cache_key)
        if cached_embedding:
            # Deserialize the cached embedding
            return json.loads(cached_embedding)
    except Exception as e:
        logging.warning(f"Redis error: {e}")

    response = await client.embeddings.create(input=[text], model=model)
    embedding = response.data[0].embedding

    # Cache the embedding in Redis
    try:
        await redis.set(cache_key, json.dumps(embedding))
    except Exception as e:
        logging.warning(f"Redis error: {e}")
        # Proceed without caching if Redis is unavailable

    return embedding
