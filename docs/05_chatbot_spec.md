# Chatbot Spec

## Objective
Provide a conversational assistant that answers questions about uploaded filings and related financial datasets.

## Message handling
- Append each user prompt to session state.
- Append each assistant response to session state.
- Keep a simple ordered history for the active session.

## Chat flow
1. User enters a question.
2. Router classifies query as narrative, numeric, or mixed.
3. App retrieves filing chunks, financial tables, or both.
4. Prompt builder constructs model input with chat history and retrieved context.
5. OpenAI generates a response.
6. Formatter renders text and optional tables.

## Output modes
### Text response
Used for summary, interpretation, and explanation.

### Table response
Used for structured financial data, comparisons, and period-over-period views.

## Behavior requirements
- Prefer concise analyst-style responses.
- Cite source sections internally even if UI citation rendering is basic in MVP.
- If numeric data is unavailable, say so clearly.
- If both uploaded filing text and Financial Datasets data exist, combine them coherently.

## Memory requirements
MVP memory is session-only:
- store user and assistant messages in `st.session_state.messages`
- preserve chat on reruns
- provide clear button to reset chat
