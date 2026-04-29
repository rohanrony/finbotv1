from typing import List, Dict

class ContextBuilder:
    """Assembles retrieved chunks into a formatted context string for LLM prompting."""
    
    def build(self, results: List[Dict]) -> str:
        """
        Format retrieval results into a single context string with metadata headers.
        """
        if not results:
            return "No relevant context found in the filings."
            
        context_parts = []
        for i, res in enumerate(results):
            meta = res["metadata"]
            header = f"--- SOURCE {i+1}: {meta.get('heading', 'Unknown Section')} ---"
            if meta.get('subheading'):
                header += f" ({meta['subheading']})"
            
            chunk_text = res["chunk_text"].strip()
            context_parts.append(f"{header}\n{chunk_text}\n")
            
        return "\n".join(context_parts)
