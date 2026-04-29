from typing import List

class DocumentChunker:
    """Chunks structured sections into smaller pieces for embedding."""
    
    def chunk_section(self, section_text: str, chunk_size: int = 1500, overlap: int = 200) -> List[str]:
        """
        Chunks text into overlapping windows.
        Simplified version for MVP.
        """
        if not section_text:
            return []
            
        chunks = []
        start = 0
        while start < len(section_text):
            end = start + chunk_size
            chunk = section_text[start:end]
            chunks.append(chunk.strip())
            
            if end >= len(section_text):
                break
            start += (chunk_size - overlap)
            
        return chunks
