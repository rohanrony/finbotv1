# Delivery Plan

## Phase 1 - Skeleton
Deliver:
- repository structure
- requirements file
- config file
- base Streamlit app shell
- tabs or pages for chat, ingestion, and library/settings
- session state initialization

## Phase 2 - Catalog and storage
Deliver:
- local file save service
- SQLite setup
- file catalog repository
- file list and metadata rendering

## Phase 3 - Ingestion pipeline
Deliver:
- loader
- text extraction
- section parser
- chunker
- table parser
- pipeline orchestration

## Phase 4 - Retrieval
Deliver:
- embeddings wrapper
- vector store
- keyword index
- hybrid retrieval service
- context builder

## Phase 5 - Chatbot
Deliver:
- Gemini client
- prompt builder
- router for narrative vs numeric questions
- answer formatter for text and table outputs

## Phase 6 - External data
Deliver:
- Financial Datasets client
- integration into query pipeline
- settings for API keys

## Phase 7 - Hardening
Deliver:
- error handling
- re-ingestion support
- reset chat action
- document preview improvements
- README and local run instructions
