# Acceptance Criteria

## Product-level acceptance
- User can upload one or more filings.
- User can assign metadata tags at upload time.
- Uploaded files appear in a file catalog view.
- User can click a file and inspect its metadata and preview.
- User can run ingestion on an uploaded file.
- Narrative sections are chunked and stored with metadata.
- Tables are parsed separately from narrative chunks.
- User can ask questions in chat and receive an answer.
- Chat can render either text or tabular output.
- Chat state persists across Streamlit reruns in the active session.
- User can enter Gemini and Financial Datasets API keys in settings.
- App runs locally and is suitable for sharing later through ngrok.

## Engineering acceptance
- Code is modular and organized by feature area.
- UI components do not contain business logic beyond orchestration.
- Ingestion can be invoked independently from UI rendering.
- Retrieval is testable as a separate module.
- External integrations are isolated behind client interfaces.
- No hard-coded secrets.

## Nice-to-have acceptance
- Reprocess file button.
- Search and filter in file catalog.
- Source references in answer metadata.
- Model and retrieval settings editable in UI.
