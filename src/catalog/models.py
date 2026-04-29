from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class FileRecord(BaseModel):
    """Represents a file record in the catalog."""
    file_id: str
    filename: str
    file_path: str
    file_hash: str
    ticker: Optional[str]
    filing_type: str
    period_label: Optional[str]
    document_year: Optional[int]
    source_type: str
    status: str
    notes: Optional[str]
    created_at: datetime

class SectionChunk(BaseModel):
    """Represents a chunk of text from a section of a filing."""
    chunk_id: str
    file_id: str
    heading: Optional[str]
    subheading: Optional[str]
    section_path: str
    chunk_index: int
    chunk_text: str
    chunk_summary: Optional[str] = None
    tags: List[str] = []
    metadata: Dict = {}

class ParsedTable(BaseModel):
    """Represents a table parsed from a filing."""
    table_id: str
    file_id: str
    section_path: Optional[str]
    table_name: Optional[str]
    dataframe_json: str
