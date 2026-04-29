# Antigravity Build Prompts

Use these prompts in order. Each prompt assumes the project already contains the spec files in `docs/` and that Antigravity can read the repository.

## Prompt 0 - Read and plan
```text
Read all markdown files in the docs/ folder and build a concise implementation plan.

Requirements:
- Summarize the architecture, module boundaries, and delivery phases.
- Do not write application code yet.
- Output:
  1. proposed folder structure,
  2. implementation sequence,
  3. dependencies list,
  4. risks and assumptions,
  5. any spec ambiguities that should be resolved before coding.
```

## Prompt 1 - Create project scaffold
```text
Read docs/00_project_overview.md, docs/01_architecture.md, docs/02_frontend_spec.md, docs/06_data_models.md, and docs/08_delivery_plan.md.

Create the initial project scaffold for a modular Streamlit app.

Tasks:
- Create folders and Python modules exactly or very close to the documented structure.
- Add placeholder classes and functions with docstrings for each major module.
- Create requirements.txt.
- Create .env.example.
- Create a minimal app.py that initializes Streamlit session state and renders empty Chat, Ingestion, and Settings/Library views.

Constraints:
- Keep business logic out of app.py.
- Use clean imports and modular boundaries.
- Do not implement full ingestion or retrieval yet.
```

## Prompt 2 - Build the UI shell
```text
Read docs/02_frontend_spec.md and docs/09_acceptance_criteria.md.

Implement the Streamlit UI shell.

Tasks:
- Build modular UI components for chat, upload/ingestion controls, library view, and settings.
- Add session-state initialization helpers.
- Support file upload widgets, metadata fields, file list rendering, and chat history rendering.
- Make the UI functional with stubbed backend calls.

Constraints:
- Use st.chat_message, st.chat_input, st.file_uploader, and session state.
- Keep all backend integrations stubbed behind service interfaces.
- Keep the UI simple and clean.
```

## Prompt 3 - Implement catalog and local storage
```text
Read docs/01_architecture.md, docs/06_data_models.md, and docs/09_acceptance_criteria.md.

Implement local persistence for uploaded files and metadata.

Tasks:
- Add a local file storage service to save uploaded files under data/uploads/.
- Add SQLite setup and migrations or initialization logic.
- Implement FileRecord persistence and retrieval.
- Connect the UI so uploaded files appear in the library/settings view.

Constraints:
- Do not implement document parsing yet.
- Keep repository and service layers separate.
- Add clear error handling for duplicate or failed uploads.
```

## Prompt 4 - Build the ingestion pipeline
```text
Read docs/03_ingestion_spec.md and docs/06_data_models.md.

Implement the ingestion pipeline in a modular way.

Tasks:
- Build loader, text extraction, section parsing, chunking, table parsing, enrichment, and pipeline orchestration modules.
- Parse headings and subheadings when possible.
- Create SectionChunk records with section_path, chunk_summary, and tags.
- Parse tables into pandas DataFrames and store them separately.
- Exclude tables from the embedding-ready narrative chunk set.
- Connect the Ingestion UI action to trigger the pipeline for a selected uploaded file.

Constraints:
- Favor readability and modularity over perfect parsing.
- Keep parser-specific logic isolated so it can be replaced later.
- Log errors without crashing the app.
```

## Prompt 5 - Add retrieval modules
```text
Read docs/04_retrieval_spec.md, docs/06_data_models.md, and docs/09_acceptance_criteria.md.

Implement hybrid retrieval.

Tasks:
- Add embeddings wrapper, vector store abstraction, keyword index, hybrid search, and context builder.
- Support metadata filters for ticker, filing type, period label, and year.
- Return retrieval results with source metadata.
- Add configuration points for top-k values and score weights.

Constraints:
- Keep vector store implementation swappable.
- Keep ranking logic explicit and easy to tune.
- Do not yet finalize the LLM answer generation prompt.
```

## Prompt 6 - Add Gemini chat pipeline
```text
Read docs/05_chatbot_spec.md and docs/07_api_integrations.md.

Implement the chatbot pipeline.

Tasks:
- Add a Gemini client module.
- Add prompt builder functions for narrative, numeric, and mixed questions.
- Add a router that decides whether to use narrative retrieval, financial retrieval, or both.
- Add answer formatting helpers that can render text or pandas DataFrames in Streamlit.
- Append user and assistant messages to session state.

Constraints:
- Keep API calls centralized in the llm/ module.
- Do not put prompt strings inline in the UI layer.
- Make it easy to change models later.
```

## Prompt 7 - Add Financial Datasets integration
```text
Read docs/07_api_integrations.md, docs/04_retrieval_spec.md, and docs/05_chatbot_spec.md.

Implement Financial Datasets integration.

Tasks:
- Add a client for Financial Datasets with clean request methods.
- Support API key configuration from settings or environment variables.
- Fetch structured financial data for numeric questions.
- Merge Financial Datasets results with uploaded filing context when appropriate.
- Render numeric outputs as tables in chat when useful.

Constraints:
- Handle missing API keys gracefully.
- Keep response normalization separate from UI rendering.
```

## Prompt 8 - Finish the library and preview experience
```text
Read docs/02_frontend_spec.md and docs/09_acceptance_criteria.md.

Improve the file catalog and preview UX.

Tasks:
- Add search and filter controls in the library.
- Show richer metadata for each file.
- Add preview support for extracted text and parsed tables.
- Add re-ingest action if a file has already been uploaded.

Constraints:
- Keep preview functionality lightweight.
- Prefer extracted text previews over complex PDF rendering for MVP.
```

## Prompt 9 - Hardening and cleanup
```text
Read all docs again and review the full codebase against the specs.

Tasks:
- Identify missing requirements.
- Refactor for modularity.
- Improve error handling and naming consistency.
- Remove dead code and duplicate logic.
- Ensure the app can be run locally with a clear README.
- Add basic tests for catalog, ingestion, and retrieval modules if appropriate.

Output:
- a change summary,
- unresolved issues,
- suggested next-step enhancements after MVP.
```

## Prompt 10 - One-shot fallback prompt
```text
Read every markdown file in docs/ and build the full MVP described there as a modular Streamlit application.

Requirements:
- Preserve the documented folder structure as much as possible.
- Build Chat, Ingestion, and Library/Settings experiences.
- Implement local upload storage, metadata cataloging, ingestion, chunking, table parsing, hybrid retrieval, Gemini integration, and Financial Datasets integration.
- Keep code modular by placing logic in src/ui, src/catalog, src/ingestion, src/retrieval, src/llm, src/integrations, and src/storage.
- Use Streamlit session state for chat memory.
- Keep the UI simple and suitable for local use and later ngrok sharing.

Before writing code:
- output a short implementation plan.

After writing code:
- output a file-by-file summary and any assumptions.
```
