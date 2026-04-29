# Project Overview

## Goal
Build a local-first Streamlit financial analyst chatbot that supports uploading S-1, 10-K, and 10-Q files, catalogs each file with user-defined metadata, ingests narrative sections into a searchable knowledge base, and answers user questions in text or tabular form.

## Primary users
- Solo builder or analyst running the app locally.
- Small internal team reviewing company filings.
- User who wants to expose the local app later via ngrok.

## Core capabilities
1. Upload one or more filing documents.
2. Add metadata tags such as ticker, filing type, fiscal period, and custom label like `2025 Q1`.
3. Persist uploaded files in a catalog and show them in a library/settings view.
4. Parse documents into sections and subsections.
5. Chunk narrative text for retrieval and ignore tabular data for embeddings.
6. Parse tables into pandas DataFrames for optional local use.
7. Fetch normalized financial data from Financial Datasets using a user-provided API key.
8. Support a chat interface with basic conversation memory.
9. Return answers as narrative text or structured tables.
10. Run locally with a simple setup and be easy to share via ngrok.

## Non-goals for MVP
- Multi-user authentication.
- Cloud deployment.
- Complex access control.
- Fine-tuned models.
- Full SEC XBRL normalization pipeline from scratch.

## Product principles
- Local-first and simple to run.
- Modular Python code with clear boundaries.
- Retrieval quality over fancy UI.
- Stable metadata and traceability for each chunk.
- Easy to extend later with more filing types and richer analytics.
