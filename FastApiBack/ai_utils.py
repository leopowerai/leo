import json
import logging

from config import settings
from openai import AsyncOpenAI
from redis_client import redis

# Set the OpenAI API key
client = AsyncOpenAI(
    # This is the default and can be omitted
    api_key=settings.OPENAI_KEY,
)


async def get_embedding(texts: str, model: str = "text-embedding-3-small") -> list:
    """
    Fetch embeddings for a single text or a list of texts.
    """
    if isinstance(texts, str):
        texts = [texts]
    cache_keys = [f"embedding:{text}" for text in texts]
    embeddings = []
    texts_to_fetch = []
    indices_to_fetch = []

    # Check cache for existing embeddings
    for i, (text, key) in enumerate(zip(texts, cache_keys)):
        try:
            cached_embedding = await redis.get(key)
            if cached_embedding:
                embeddings.append(json.loads(cached_embedding))
            else:
                embeddings.append(None)
                texts_to_fetch.append(text)
                indices_to_fetch.append(i)
        except Exception as e:
            logging.warning(f"Redis error: {e}")
            embeddings.append(None)
            texts_to_fetch.append(text)
            indices_to_fetch.append(i)

    # Fetch embeddings for texts not in cache
    if texts_to_fetch:
        try:
            response = await client.embeddings.create(input=texts_to_fetch, model=model)
            fetched_embeddings = [item.embedding for item in response.data]

            # Cache fetched embeddings
            for idx, embedding in zip(indices_to_fetch, fetched_embeddings):
                embeddings[idx] = embedding
                cache_key = cache_keys[idx]
                try:
                    await redis.set(cache_key, json.dumps(embedding))
                except Exception as e:
                    logging.warning(f"Redis error when caching: {e}")
        except Exception as e:
            logging.error(f"Error fetching embeddings from OpenAI: {e}")
            raise

    return embeddings if len(embeddings) > 1 else embeddings[0]
