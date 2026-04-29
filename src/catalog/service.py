import uuid
from typing import List, Optional, Tuple
from datetime import datetime
from src.catalog.models import FileRecord
from src.catalog.repository import CatalogRepository
from src.storage.files import FileStorage

class CatalogService:
    """Orchestrates catalog and storage operations."""
    def __init__(self, repository: CatalogRepository, file_storage: FileStorage):
        self.repository = repository
        self.file_storage = file_storage

    def upload_file(self, filename: str, content: bytes, metadata: dict) -> Tuple[bool, str]:
        """
        Handles file upload: saves to disk and records in database.
        Returns (success, message).
        """
        # 1. Save file to disk and get hash
        file_path, file_hash = self.file_storage.save_file(filename, content)
        
        # 2. Check for duplicate hash
        existing = self.repository.get_file_by_hash(file_hash)
        if existing:
            return False, f"File already exists in catalog (ID: {existing.file_id})"

        # 3. Create FileRecord
        file_id = str(uuid.uuid4())
        new_record = FileRecord(
            file_id=file_id,
            filename=filename,
            file_path=file_path,
            file_hash=file_hash,
            ticker=metadata.get("ticker"),
            filing_type=metadata.get("filing_type", "Other"),
            period_label=metadata.get("period_label"),
            document_year=metadata.get("document_year"),
            source_type="Upload",
            status="Uploaded",
            notes=metadata.get("notes"),
            created_at=datetime.now()
        )

        # 4. Save to database
        success = self.repository.add_file(new_record)
        if success:
            return True, f"Successfully uploaded {filename}"
        else:
            # Cleanup file if DB insert fails
            self.file_storage.delete_file(file_path)
            return False, "Failed to record file in database."

    def list_files(self) -> List[FileRecord]:
        """List all files available in the catalog."""
        return self.repository.get_all_files()

    def delete_file(self, file_id: str) -> bool:
        """Deletes a file from both catalog and storage."""
        record = self.repository.get_file_by_id(file_id)
        if record:
            self.file_storage.delete_file(record.file_path)
            self.repository.delete_file(file_id)
            return True
        return False

    def get_file_content_preview(self, file_id: str) -> List[dict]:
        """Fetch chunk contents for preview."""
        chunks = self.repository.get_chunks_by_file_id(file_id)
        return [dict(row) for row in chunks]

    def get_file_tables(self, file_id: str) -> List[dict]:
        """Fetch parsed tables for preview."""
        tables = self.repository.get_tables_by_file_id(file_id)
        return [dict(row) for row in tables]

    def reset_file_status(self, file_id: str):
        """Resets file status to 'Uploaded' for re-ingestion."""
        self.repository.update_file_status(file_id, 'Uploaded')
