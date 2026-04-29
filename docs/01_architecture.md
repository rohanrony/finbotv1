# Architecture Spec

## High-level design
The system is a modular Streamlit application with five main layers:

1. Presentation layer: Streamlit UI for upload, chat, library, and settings.
2. Application layer: orchestration services for ingestion, retrieval, and chat.
3. Storage layer: local filesystem plus SQLite for metadata and chat state.
4. Retrieval layer: embeddings, vector index, keyword index, and metadata filters.
5. Integration layer: OpenAI API and Financial Datasets API.

## End-to-end flow
1. User uploads a file and enters tags.
2. App saves the file to `data/uploads/` and creates a catalog record.
3. Ingestion pipeline extracts text, identifies sections, parses tables, and creates chunks.
4. Narrative chunks are enriched with headings, subheadings, descriptions, and tags.
5. Chunks are embedded and stored in vector storage.
6. Keyword fields and metadata are stored for hybrid search.
7. User asks a question in chat.
8. Router decides whether to use filing chunk retrieval, Financial Datasets API, or both.
9. Context builder assembles narrative chunks and optional financial tables.
10. OpenAI generates a final answer in text or table-ready format.
11. Response and user message are appended to session state and persisted if desired.

## Architectural constraints
- Local filesystem must be the source of truth for files.
- SQLite must store document catalog metadata.
- Streamlit session state must maintain current chat state.
- API keys must be provided through settings or environment variables.
- The ingestion pipeline must be callable independently from the UI.

## Suggested implementation style
- Thin UI layer.
- Service classes or pure functions for business logic.
- Repository pattern for persistence.
- Clear dataclasses or pydantic models for transfer objects.
