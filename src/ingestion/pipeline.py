import uuid
import json
from src.ingestion.loader import DocumentLoader
from src.ingestion.section_parser import SectionParser
from src.ingestion.chunker import DocumentChunker
from src.ingestion.table_parser import TableParser
from src.storage.sqlite import SQLiteManager
from src.retrieval.embeddings import EmbeddingProvider
from src.retrieval.vector_store import VectorStore

class IngestionPipeline:
    """Orchestrates the full ingestion process including vector storage."""
    def __init__(
        self, 
        db_manager: SQLiteManager, 
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore
    ):
        self.loader = DocumentLoader()
        self.parser = SectionParser()
        self.chunker = DocumentChunker()
        self.table_parser = TableParser()
        self.db_manager = db_manager
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store

    def process_file(self, file_id: str, file_path: str) -> bool:
        """Run the full ingestion pipeline on a file."""
        try:
            # 0. Get file metadata for vector storage
            file_meta = self.db_manager.execute_query("SELECT * FROM file_records WHERE file_id = ?", (file_id,))[0]
            base_metadata = {
                "file_id": file_id,
                "ticker": file_meta["ticker"] or "N/A",
                "filing_type": file_meta["filing_type"],
                "year": str(file_meta["document_year"])
            }

            # 1. Load and Extract Text
            text = self.loader.load_pdf(file_path)
            
            # 2. Parse into Sections
            sections = self.parser.parse(text)
            
            # 3. Chunk, Embed, and Store
            all_chunks_for_vector_store = []
            
            for section in sections:
                chunks = self.chunker.chunk_section(section["text"])
                for i, chunk_text in enumerate(chunks):
                    chunk_id = str(uuid.uuid4())
                    
                    # Store in SQLite
                    chunk_data = {
                        "chunk_id": chunk_id,
                        "file_id": file_id,
                        "heading": section["heading"],
                        "subheading": section["subheading"],
                        "section_path": section["heading"],
                        "chunk_index": i,
                        "chunk_text": chunk_text,
                        "chunk_summary": None,
                        "tags": json.dumps([]),
                        "metadata": json.dumps(base_metadata)
                    }
                    self.db_manager.insert_chunk(chunk_data)
                    
                    # Prepare for Vector Store
                    all_chunks_for_vector_store.append({
                        "chunk_id": chunk_id,
                        "chunk_text": chunk_text,
                        "metadata": {**base_metadata, "heading": section["heading"]}
                    })

            # Batch Embedding and Vector Storage
            if all_chunks_for_vector_store:
                texts = [c["chunk_text"] for c in all_chunks_for_vector_store]
                embeddings = self.embedding_provider.get_embeddings(texts)
                self.vector_store.add_chunks(all_chunks_for_vector_store, embeddings)
            
            # 4. Extract and Store Tables
            tables = self.table_parser.extract_tables(file_path)
            for i, df in enumerate(tables):
                table_data = {
                    "table_id": str(uuid.uuid4()),
                    "file_id": file_id,
                    "section_path": None,
                    "table_name": f"Table {i+1}",
                    "dataframe_json": df.to_json(orient='records')
                }
                self.db_manager.insert_table(table_data)

            # 5. Update File Status
            self.db_manager.execute_commit(
                "UPDATE file_records SET status = ? WHERE file_id = ?",
                ("Ingested", file_id)
            )
            return True
            
        except Exception as e:
            print(f"Error processing file {file_id}: {e}")
            self.db_manager.execute_commit(
                "UPDATE file_records SET status = ? WHERE file_id = ?",
                (f"Error: {str(e)[:50]}", file_id)
            )
            return False
