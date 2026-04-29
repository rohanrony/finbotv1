# Frontend Spec

## Framework
Use Streamlit because it provides built-in support for file upload, tabs or multipage layouts, chat elements, and session state.

## Main screens
### Chat
Purpose:
- Show conversation history.
- Accept user prompts.
- Render text and table responses.

Requirements:
- Use `st.chat_message` for user and assistant messages.
- Use `st.chat_input` for prompt entry.
- Render DataFrame outputs with `st.dataframe`.
- Show citations or source references later as expandable metadata.

### Ingestion
Purpose:
- Upload files.
- Enter metadata tags.
- Trigger ingestion.

Requirements:
- Use `st.file_uploader` with support for multiple files.
- Show metadata fields: ticker, filing type, fiscal period label, document year, optional notes.
- Provide an `Ingest` button.
- Show status indicators: uploaded, queued, processed, failed.

### Library / Settings
Purpose:
- Show uploaded files.
- Manage keys and app settings.
- Preview selected documents.

Requirements:
- Display file list with search and filters.
- Allow selecting a file to view metadata and preview text.
- Show API key fields for Gemini and Financial Datasets.
- Include toggles for retrieval settings, top-k, and model selection if needed.

## Navigation
Preferred MVP choices:
- Single-page app with top-level tabs, or
- Multipage Streamlit app using a homepage plus `pages/` directory.

Use whichever keeps implementation simpler, but keep UI modules separated even if rendered in one file.

## Session state
The UI must initialize and manage:
- `messages`
- `selected_file_id`
- `filters`
- `settings`
- `ingestion_jobs`

## UX notes
- Keep chat pane visually primary.
- Put upload and settings in sidebars, tabs, or separate sections.
- Make file catalog easy to scan by ticker, period, and filing type.
