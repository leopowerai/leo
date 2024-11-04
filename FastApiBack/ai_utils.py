import json
import os

import openai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_KEY")

# Function to obtain text embeddings using OpenAI


# def get_embedding(text: str, model: str = "text-embedding-ada-002") -> list:
#     """
#     Generate an embedding vector for a given text using the specified model.

#     Args:
#         text (str): Text to embed.
#         model (str): Model name for generating embeddings.

#     Returns:
#         list: Embedding vector of the text.
#     """
#     # The input is now wrapped as a list (e.g., `[text]`)
#     response = openai.embeddings.create(input=[text], model=model)
#     return response.data[0].embedding


def get_embedding(text: str, model: str = "text-embedding-3-small") -> list:
    # Check if the embedding exists in the cache file
    if os.path.exists("embeddings_cache.json"):
        with open("embeddings_cache.json", "r") as file:
            embeddings_cache = json.load(file)
    else:
        embeddings_cache = {}

    # Return cached embedding if available
    if text in embeddings_cache:
        return embeddings_cache[text]

    # Otherwise, fetch from API
    response = openai.embeddings.create(input=[text], model=model)
    embedding = response.data[0].embedding

    # Save the new embedding in the cache
    embeddings_cache[text] = embedding
    with open("embeddings_cache.json", "w") as file:
        json.dump(embeddings_cache, file)

    return embedding
