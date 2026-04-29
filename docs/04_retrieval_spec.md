# Retrieval Spec

## Objective
Provide hybrid retrieval over uploaded filing chunks using semantic similarity, keyword matching, and metadata filters.

## Retrieval modes
### Narrative retrieval
Use for qualitative questions such as:
- summarize risk factors
- what changed in management discussion
- what does the company say about liquidity

Method:
- semantic search over chunk embeddings
- keyword boost on headings, subheadings, section paths, and tags
- metadata filters on ticker, filing type, period, and year

### Financial retrieval
Use for quantitative questions such as:
- show revenue trend
- compare total assets
- list operating cash flow for recent quarters

Method:
- call Financial Datasets API first
- optionally combine with filing chunk context if the user asks for narrative explanation

## Hybrid ranking formula
Use a simple weighted strategy for MVP:
- semantic score
- keyword score
- metadata match boost
- recency or exact-period boost if relevant

## Context assembly rules
- Deduplicate overlapping chunks.
- Prefer diversity across sections.
- Preserve source metadata for each returned chunk.
- Keep final prompt context bounded.

## Retrieval configuration
Configurable settings:
- top-k semantic results
- top-k final contexts
- keyword weight
- metadata weight
- chunk overlap
