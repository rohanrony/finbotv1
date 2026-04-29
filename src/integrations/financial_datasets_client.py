import requests
import os
from typing import Dict, List, Optional

class FinancialDatasetsClient:
    """Client for the Financial Datasets API."""
    
    BASE_URL = "https://api.financialdatasets.ai"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("FINANCIAL_DATASETS_API_KEY") or os.getenv("FINANCIAL_DATASETS_AI_API_KEY")

    def _get_headers(self):
        return {"X-API-KEY": self.api_key}

    def get_financials(self, ticker: str, period: str = "annual", limit: int = 30) -> Dict:
        """
        Fetch income statement, balance sheet, and cash flow data.
        """
        if not self.api_key:
            return {"error": "Financial Datasets API key not configured."}

        # Adding trailing slash as per documentation example
        url = f"{self.BASE_URL}/financials/"
        params = {
            "ticker": ticker,
            "period": period,
            "limit": limit
        }
        
        try:
            response = requests.get(url, params=params, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_filing_items(self, ticker: str, filing_type: str, item_names: List[str]) -> List[Dict]:
        """
        Fetch specific items from a filing (e.g., 'revenue', 'net_income').
        """
        if not self.api_key:
            return []

        url = f"{self.BASE_URL}/filings/items"
        params = {
            "ticker": ticker,
            "filing_type": filing_type,
            "item_names": ",".join(item_names)
        }
        
        try:
            response = requests.get(url, params=params, headers=self._get_headers())
            response.raise_for_status()
            return response.json().get("items", [])
        except Exception as e:
            print(f"Error fetching filing items: {e}")
            return []
