# Ingestion Spec

## Objective
Convert an uploaded filing into structured sections, narrative chunks, parsed tables, and searchable metadata.

## Supported inputs
- PDF
- HTML / HTM
- TXT

## Ingestion steps
1. Save uploaded file.
2. Compute file hash and basic metadata.
3. Extract raw text.
4. Detect major sections and subsections.
5. Parse tables where possible into pandas DataFrames.
6. Exclude tables from narrative embedding chunks.
7. Chunk narrative text using section-aware logic.
8. Create retrieval metadata for each chunk.
9. Embed chunk text.
10. Persist chunk records and vector references.

## Section parsing rules
- Prefer heading-aware splitting.
- Preserve hierarchy like `Item 1A > Risk Factors` or `Item 2 > MD&A > Liquidity`.
- Keep section path on every chunk.
- Store original text offsets if available.

## Chunking rules
- Chunk by section and subsection first.
- Use max token or character thresholds only as fallback.
- Keep overlap modest for continuity.
- Each chunk must include:
  - chunk id
  - file id
  - heading
  - subheading
  - section path
  - chunk text
  - short description
  - tags

## Tagging rules
Auto-attach tags from:
- ticker
- filing type
- period label
- document year
- section heading
- subsection heading
- custom tags entered by the user

## Table handling rules
- Parse tables into DataFrames when feasible.
- Store tables separately from narrative chunks.
- Do not embed table cells in the narrative vector index.
- Allow local rendering of parsed tables in previews or answers.

## Error handling
- Mark ingestion status per file.
- Log parser failures.
- Allow reprocessing a file.
