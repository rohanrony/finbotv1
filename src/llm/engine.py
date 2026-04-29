import json
import pandas as pd
from typing import List, Dict, Tuple, Optional
from src.llm.llm_client import LLMClient
from src.llm.prompts import build_narrative_prompt, build_routing_prompt, build_ticker_extraction_prompt
from src.retrieval.hybrid_search import HybridSearchEngine
from src.retrieval.context_builder import ContextBuilder
from src.integrations.financial_datasets_client import FinancialDatasetsClient

class ChatbotEngine:
    """Coordinates query routing, retrieval, and response generation."""
    
    def __init__(
        self, 
        llm_client: LLMClient, 
        hybrid_search: HybridSearchEngine,
        context_builder: ContextBuilder,
        financial_datasets: Optional[FinancialDatasetsClient] = None
    ):
        self.llm_client = llm_client
        self.hybrid_search = hybrid_search
        self.context_builder = context_builder
        self.financial_datasets = financial_datasets

    def route_query(self, query: str) -> str:
        """Classify the query into NARRATIVE, NUMERIC, or MIXED."""
        # Fast-track numeric queries with keywords
        financial_keywords = ["revenue", "income", "profit", "sales", "eps", "margin", "asset", "liability", "debt", "cash"]
        query_lower = query.lower()
        if any(kw in query_lower for kw in financial_keywords):
            # If it has financial keywords, it's at least MIXED or NUMERIC
            prompt = build_routing_prompt(query)
            category = self.llm_client.generate_answer(prompt).strip().upper()
            if "NUMERIC" in category: return "NUMERIC"
            return "MIXED"

        prompt = build_routing_prompt(query)
        category = self.llm_client.generate_answer(prompt).strip().upper()
        # Clean up category string in case LLM adds fluff
        for cat in ["NARRATIVE", "NUMERIC", "MIXED"]:
            if cat in category:
                return cat
        return "NARRATIVE"

    def extract_ticker(self, query: str) -> Optional[str]:
        """Extracts a stock ticker from the query using the LLM."""
        prompt = build_ticker_extraction_prompt(query)
        ticker = self.llm_client.generate_answer(prompt).strip().upper()
        # Clean up common fluff (periods, quotes, "Ticker: ")
        ticker = ticker.replace("TICKER:", "").replace("\"", "").replace("'", "").replace(".", "").strip()
        if "NONE" in ticker or len(ticker) > 5 or not ticker:
            return None
        return ticker

    def ask(self, query: str, history: List[Dict], filters: Dict = None) -> Tuple[str, List[Dict], Optional[str]]:
        """
        Processes a user query and returns (answer, search_results, table_json).
        """
        # 1. Route query
        category = self.route_query(query)
        print(f"[DEBUG] Query category: {category}")
        
        # 2. Extract Ticker if not provided
        if filters is None:
            filters = {}
            
        ticker = filters.get("ticker")
        if not ticker:
            ticker = self.extract_ticker(query)
            print(f"[DEBUG] Extracted ticker: {ticker}")
            if ticker:
                filters["ticker"] = ticker
        
        context = ""
        search_results = []
        table_json = None
        
        # 3. Retrieve Financial Data
        # Trigger if explicitly numeric/mixed OR if we found a ticker and query has financial keywords
        financial_keywords = ["revenue", "income", "profit", "sales", "eps", "margin", "asset", "liability", "debt", "cash"]
        is_financial_query = any(kw in query.lower() for kw in financial_keywords)
        
        if (category in ["NUMERIC", "MIXED"] or is_financial_query) and self.financial_datasets and ticker:
            print(f"[DEBUG] Calling Financial Datasets API for {ticker}")
            response_data = self.financial_datasets.get_financials(ticker)
            
            if "error" not in response_data:
                # API can return data nested under "financials" or at the top level
                financial_data = response_data.get("financials", response_data)
                
                # Convert to context string for LLM
                context += "\n" + "="*50 + "\n"
                context += f"EXTERNAL FINANCIAL DATA (API) FOR {ticker}:\n"
                context += "="*50 + "\n"
                context += json.dumps(financial_data, indent=2)
                context += "\n" + "="*50 + "\n"
                print(f"[DEBUG] API Data added to context. Length: {len(context)}")
                
                # Extract for table rendering if possible
                income_statements = financial_data.get("income_statements", [])
                if income_statements:
                    df = pd.DataFrame(income_statements)
                    # Keep only relevant columns for the UI table
                    cols = ["ticker", "calendar_year", "report_period", "revenue", "net_income", "eps_diluted"]
                    available_cols = [c for c in cols if c in df.columns]
                    if available_cols:
                        table_json = df[available_cols].to_json(orient='records')
                    else:
                        table_json = df.to_json(orient='records')
            else:
                print(f"[DEBUG] API Error: {response_data['error']}")

        # 4. Retrieve Narrative Context
        # Passing filters helps target the search to the correct company
        search_results = self.hybrid_search.search(query, filters=filters)
        narrative_context = self.context_builder.build(search_results)
        context += f"\n\nFILING TEXT CONTEXT:\n{narrative_context}"
        
        # 5. Build Prompt
        full_prompt = build_narrative_prompt(query, context, history)
        
        # 6. Generate Answer
        answer = self.llm_client.generate_answer(full_prompt)
        
        return answer, search_results, table_json
