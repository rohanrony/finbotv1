import sqlite3
import os
from typing import List, Optional

class SQLiteManager:
    """Manages connection and basic operations for the SQLite database."""
    def __init__(self, db_path: str = "data/app.db"):
        self.db_path = db_path
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.initialize_db()

    def get_connection(self):
        """Returns a sqlite3 connection with row factory enabled."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def initialize_db(self):
        """Create tables if they don't exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # FileRecord table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS file_records (
                    file_id TEXT PRIMARY KEY,
                    filename TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    file_hash TEXT NOT NULL UNIQUE,
                    ticker TEXT,
                    filing_type TEXT NOT NULL,
                    period_label TEXT,
                    document_year INTEGER,
                    source_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    notes TEXT,
                    created_at TEXT NOT NULL
                )
            """)
            # SectionChunk table (placeholder for next phases)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS section_chunks (
                    chunk_id TEXT PRIMARY KEY,
                    file_id TEXT NOT NULL,
                    heading TEXT,
                    subheading TEXT,
                    section_path TEXT,
                    chunk_index INTEGER,
                    chunk_text TEXT,
                    chunk_summary TEXT,
                    tags TEXT,
                    metadata TEXT,
                    FOREIGN KEY (file_id) REFERENCES file_records (file_id)
                )
            """)
            # ParsedTable table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS parsed_tables (
                    table_id TEXT PRIMARY KEY,
                    file_id TEXT NOT NULL,
                    section_path TEXT,
                    table_name TEXT,
                    dataframe_json TEXT,
                    FOREIGN KEY (file_id) REFERENCES file_records (file_id)
                )
            """)
            conn.commit()

    def execute_query(self, query: str, params: tuple = ()):
        """Executes a query and returns results."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute_commit(self, query: str, params: tuple = ()):
        """Executes a query and commits the transaction."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid

    def insert_chunk(self, chunk_data: dict):
        """Inserts a single section chunk into the database."""
        query = """
            INSERT INTO section_chunks (
                chunk_id, file_id, heading, subheading, section_path,
                chunk_index, chunk_text, chunk_summary, tags, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            chunk_data["chunk_id"], chunk_data["file_id"], chunk_data["heading"],
            chunk_data["subheading"], chunk_data["section_path"],
            chunk_data["chunk_index"], chunk_data["chunk_text"],
            chunk_data["chunk_summary"], chunk_data["tags"], chunk_data["metadata"]
        )
        self.execute_commit(query, params)

    def insert_table(self, table_data: dict):
        """Inserts a parsed table record into the database."""
        # Note: ParsedTable table might need to be created if not in init
        query = """
            INSERT INTO parsed_tables (
                table_id, file_id, section_path, table_name, dataframe_json
            ) VALUES (?, ?, ?, ?, ?)
        """
        params = (
            table_data["table_id"], table_data["file_id"], table_data["section_path"],
            table_data["table_name"], table_data["dataframe_json"]
        )
        self.execute_commit(query, params)

    def get_chunks_by_file_id(self, file_id: str) -> List[sqlite3.Row]:
        """Fetch all chunks for a specific file."""
        return self.execute_query("SELECT * FROM section_chunks WHERE file_id = ? ORDER BY chunk_index", (file_id,))

    def get_tables_by_file_id(self, file_id: str) -> List[sqlite3.Row]:
        """Fetch all tables for a specific file."""
        return self.execute_query("SELECT * FROM parsed_tables WHERE file_id = ?", (file_id,))
