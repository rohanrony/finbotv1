# API Integrations

## OpenAI
Purpose:
- answer user questions
- summarize chunks if needed
- optionally generate chunk descriptions

Requirements:
- support API key from environment or UI settings
- centralize model calls in one client module
- expose methods for `generate_answer()` and optional helper methods

## Financial Datasets
Purpose:
- retrieve normalized or source filing financial data for 10-K and 10-Q analysis
- support tabular answers without depending on PDF table extraction

Requirements:
- support API key input from settings
- centralize requests in a single client module
- methods may include:
  - get_filings
  - get_filing_items
  - get_financials_by_ticker_and_period

## Integration rules
- keep external API code out of the UI layer
- normalize all responses before use downstream
- fail gracefully with clear user-visible errors
