from typing import List, Optional
from src.catalog.models import FileRecord
from src.storage.sqlite import SQLiteManager
from datetime import datetime

class CatalogRepository:
    """Handles data access for the file catalog using SQLite."""
    def __init__(self, db_manager: SQLiteManager):
        self.db_manager = db_manager

    def get_all_files(self) -> List[FileRecord]:
        """Retrieve all file records from the database."""
        rows = self.db_manager.execute_query("SELECT * FROM file_records ORDER BY created_at DESC")
        return [self._row_to_model(row) for row in rows]

    def get_file_by_id(self, file_id: str) -> Optional[FileRecord]:
        """Retrieve a single file record by ID."""
        rows = self.db_manager.execute_query("SELECT * FROM file_records WHERE file_id = ?", (file_id,))
        if rows:
            return self._row_to_model(rows[0])
        return None

    def get_file_by_hash(self, file_hash: str) -> Optional[FileRecord]:
        """Retrieve a file record by its hash."""
        rows = self.db_manager.execute_query("SELECT * FROM file_records WHERE file_hash = ?", (file_hash,))
        if rows:
            return self._row_to_model(rows[0])
        return None

    def add_file(self, file: FileRecord) -> bool:
        """Add a new file record to the catalog."""
        try:
            self.db_manager.execute_commit("""
                INSERT INTO file_records (
                    file_id, filename, file_path, file_hash, ticker, 
                    filing_type, period_label, document_year, 
                    source_type, status, notes, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                file.file_id, file.filename, file.file_path, file.file_hash, 
                file.ticker, file.filing_type, file.period_label, 
                file.document_year, file.source_type, file.status, 
                file.notes, file.created_at.isoformat()
            ))
            return True
        except Exception as e:
            print(f"Error adding file to catalog: {e}")
            return False

    def delete_file(self, file_id: str):
        """Deletes a file record from the database."""
        self.db_manager.execute_commit("DELETE FROM file_records WHERE file_id = ?", (file_id,))

    def get_chunks_by_file_id(self, file_id: str):
        """Fetch all chunks for a specific file."""
        return self.db_manager.get_chunks_by_file_id(file_id)

    def get_tables_by_file_id(self, file_id: str):
        """Fetch all tables for a specific file."""
        return self.db_manager.get_tables_by_file_id(file_id)

    def update_file_status(self, file_id: str, status: str):
        """Updates the status of a file record."""
        self.db_manager.execute_commit(
            "UPDATE file_records SET status = ? WHERE file_id = ?",
            (status, file_id)
        )

    def _row_to_model(self, row) -> FileRecord:
        """Converts a SQLite Row to a FileRecord model."""
        return FileRecord(
            file_id=row["file_id"],
            filename=row["filename"],
            file_path=row["file_path"],
            file_hash=row["file_hash"],
            ticker=row["ticker"],
            filing_type=row["filing_type"],
            period_label=row["period_label"],
            document_year=row["document_year"],
            source_type=row["source_type"],
            status=row["status"],
            notes=row["notes"],
            created_at=datetime.fromisoformat(row["created_at"])
        )
