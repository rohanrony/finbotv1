# Data Models

## FileRecord
```python
FileRecord(
    file_id: str,
    filename: str,
    file_path: str,
    file_hash: str,
    ticker: str | None,
    filing_type: str,
    period_label: str | None,
    document_year: int | None,
    source_type: str,
    status: str,
    notes: str | None,
    created_at: str,
)
```

## SectionChunk
```python
SectionChunk(
    chunk_id: str,
    file_id: str,
    heading: str | None,
    subheading: str | None,
    section_path: str,
    chunk_index: int,
    chunk_text: str,
    chunk_summary: str | None,
    tags: list[str],
    metadata: dict,
)
```

## ParsedTable
```python
ParsedTable(
    table_id: str,
    file_id: str,
    section_path: str | None,
    table_name: str | None,
    dataframe_json: str,
)
```

## ChatMessage
```python
ChatMessage(
    role: str,
    content: str,
    message_type: str = "text",
    table_payload: dict | None = None,
    timestamp: str | None = None,
)
```

## Settings
```python
AppSettings(
    gemini_api_key: str | None,
    financial_datasets_api_key: str | None,
    default_model: str,
    top_k: int,
    use_financial_datasets: bool,
)
```
