test_files = {
    "ticker":"AAPL",
    "document_year":2026,
    "period_label": "Q1 2026",
    "filing_type": "10-Q"
}

class TestConfig:
    def __init__(self):
        self.ticker = "AAPL"
        self.filing_type = "10-Q"
        self.period_label = "Q1 2026"
        self.document_year = 2026
        self.search_filters = {
            "ticker": "AAPL",
            "filing_type": "10-Q",
            "period_label": "Q1 2026",
            "document_year": 2026
        }
        self.page_size = 5
        self.top_k = 5