from src.storage.sqlite import SQLiteManager
from typing import List, Dict

class KeywordIndex:
    """Provides keyword-based search over stored chunks using SQLite."""
    
    def __init__(self, db_manager: SQLiteManager):
        self.db_manager = db_manager

    def search(self, query: str, filters: Dict = None, top_k: int = 10) -> List[Dict]:
        """
        Perform keyword search using SQL LIKE on chunk_text and headings.
        """
        sql = """
            SELECT sc.*, fr.ticker, fr.filing_type 
            FROM section_chunks sc
            JOIN file_records fr ON sc.file_id = fr.file_id
            WHERE sc.chunk_text LIKE ?
        """
        params = [f"%{query}%"]
        
        if filters:
            for key, value in filters.items():
                if not value:
                    continue
                
                # Map filters to correct table
                table_prefix = "fr" if key in ["ticker", "filing_type"] else "sc"
                
                if isinstance(value, list):
                    placeholders = ",".join(["?"] * len(value))
                    sql += f" AND {table_prefix}.{key} IN ({placeholders})"
                    params.extend(value)
                else:
                    sql += f" AND {table_prefix}.{key} = ?"
                    params.append(value)
        
        sql += f" LIMIT {top_k}"
        
        rows = self.db_manager.execute_query(sql, tuple(params))
        
        results = []
        for row in rows:
            results.append({
                "chunk_id": row["chunk_id"],
                "chunk_text": row["chunk_text"],
                "metadata": {
                    "file_id": row["file_id"],
                    "heading": row["heading"],
                    "subheading": row["subheading"],
                    "section_path": row["section_path"]
                },
                "score": 1.0 # Constant score for keyword matches for now
            })
            
        return results
