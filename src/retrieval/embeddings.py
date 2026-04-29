import openai
import os
from typing import List, Optional

class EmbeddingProvider:
    """Generates vector embeddings for text using OpenAI."""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "text-embedding-3-small"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model_name = model_name
        if self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def get_embedding(self, text: str) -> List[float]:
        """Generate an embedding for a single text string."""
        if not self.api_key or not self.client:
            return [0.0] * 1536 # OpenAI small embedding dimension
            
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.model_name
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"OpenAI Embedding Error: {e}")
            raise e

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of text strings."""
        if not self.api_key or not self.client:
            return [[0.0] * 1536 for _ in texts]
            
        try:
            response = self.client.embeddings.create(
                input=texts,
                model=self.model_name
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            print(f"OpenAI Embedding Error: {e}")
            raise e
