import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict, Optional

class VectorStore:
    """Handles storage and semantic similarity search of text chunks using ChromaDB."""
    
    def __init__(self, persist_directory: str = "data/vectors"):
        self.persist_directory = persist_directory
        os.makedirs(self.persist_directory, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection = self.client.get_or_create_collection(name="filing_chunks")

    def add_chunks(self, chunks: List[Dict], embeddings: List[List[float]]):
        """
        Add chunks and their embeddings to the store.
        chunks: List of dicts with 'chunk_id', 'chunk_text', and 'metadata'.
        """
        ids = [c["chunk_id"] for c in chunks]
        documents = [c["chunk_text"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]
        
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

    def search(self, query_embedding: List[float], filters: Optional[Dict] = None, top_k: int = 5) -> List[Dict]:
        """
        Perform semantic search.
        filters: Dictionary for metadata filtering (e.g., {"ticker": "AAPL"}).
        """
        where = None
        if filters:
            filter_clauses = []
            for key, value in filters.items():
                if not value:
                    continue
                if isinstance(value, list):
                    # ChromaDB uses $in for list values
                    filter_clauses.append({key: {"$in": value}})
                else:
                    filter_clauses.append({key: value})
            
            if len(filter_clauses) > 1:
                where = {"$and": filter_clauses}
            elif len(filter_clauses) == 1:
                where = filter_clauses[0]

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where
        )
        
        formatted_results = []
        if results["ids"]:
            for i in range(len(results["ids"][0])):
                formatted_results.append({
                    "chunk_id": results["ids"][0][i],
                    "chunk_text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "score": results["distances"][0][i] # In Chroma, lower is better (distance)
                })
        
        return formatted_results
    
    def delete_by_file_id(self, file_id: str):
        """Delete all chunks associated with a specific file ID."""
        self.collection.delete(where={"file_id": file_id})
