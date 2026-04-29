from typing import List, Dict, Optional
from src.retrieval.embeddings import EmbeddingProvider
from src.retrieval.vector_store import VectorStore
from src.retrieval.keyword_index import KeywordIndex

class HybridSearchEngine:
    """Combines semantic search and keyword search results with metadata filtering."""
    
    def __init__(
        self, 
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
        keyword_index: KeywordIndex
    ):
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store
        self.keyword_index = keyword_index

    def search(
        self, 
        query: str, 
        filters: Optional[Dict] = None, 
        top_k: int = 5,
        semantic_weight: float = 0.7,
        keyword_weight: float = 0.3
    ) -> List[Dict]:
        """
        Perform hybrid search and merge results.
        """
        # 1. Semantic Search
        query_embedding = self.embedding_provider.get_embedding(query)
        semantic_results = self.vector_store.search(query_embedding, filters=filters, top_k=top_k * 2)
        
        # 2. Keyword Search
        keyword_results = self.keyword_index.search(query, filters=filters, top_k=top_k * 2)
        
        # 3. Combine and Rank
        combined = {}
        
        # Add semantic results
        for i, res in enumerate(semantic_results):
            cid = res["chunk_id"]
            # Score normalized (simplified: 1/distance)
            score = (1.0 / (1.0 + res["score"])) * semantic_weight
            combined[cid] = {**res, "combined_score": score}
            
        # Add keyword results
        for res in keyword_results:
            cid = res["chunk_id"]
            score = res["score"] * keyword_weight
            if cid in combined:
                combined[cid]["combined_score"] += score
            else:
                combined[cid] = {**res, "combined_score": score}
                
        # Sort by combined score
        ranked = sorted(combined.values(), key=lambda x: x["combined_score"], reverse=True)
        
        return ranked[:top_k]
