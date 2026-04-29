from typing import List, Dict

SYSTEM_PROMPT = """You are an expert Financial Analyst AI. 
Your task is to answer questions about company filings (10-K, 10-Q, S-1) and financial data.
Current Date: 2026-04-28
Guidelines:
- Be concise and professional.
- Use tabular format for financial data comparisons if requested.
- If the answer is not in the context or provided API data, say so clearly.
- Cite the source sections (e.g., 'Item 1', 'Item 7') when using filing context.
- **IMPORTANT**: If external financial data (API DATA) is provided, prioritize it over your internal knowledge. Use it to answer quantitative questions about revenue, net income, etc.
"""

def build_narrative_prompt(query: str, context: str, history: List[Dict]) -> str:
    """Builds a prompt for qualitative/narrative questions."""
    history_str = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in history[-5:]])
    
    prompt = f"{SYSTEM_PROMPT}\n\n"
    prompt += f"CHAT HISTORY:\n{history_str}\n\n"
    prompt += f"CONTEXT FROM FILINGS:\n{context}\n\n"
    prompt += f"USER QUESTION: {query}\n\n"
    prompt += "ANALYST RESPONSE:"
    return prompt

def build_routing_prompt(query: str) -> str:
    """Prompt for classifying the user query."""
    return f"""Classify the following financial query into one of three categories:
1. NARRATIVE: Qualitative questions about business, risk, management discussion, etc.
2. NUMERIC: Quantitative questions about revenue, assets, margins, specific line items.
3. MIXED: Both qualitative and quantitative.

Query: "{query}"

Output only the category name (NARRATIVE, NUMERIC, or MIXED)."""

def build_ticker_extraction_prompt(query: str) -> str:
    """Prompt for extracting the stock ticker from a query."""
    return f"""Extract the primary stock ticker symbol from the following financial query.

Query: "{query}"

Guidelines:
- If a company name is mentioned (e.g., "Apple"), return its ticker (e.g., "AAPL").
- If a ticker is mentioned (e.g., "NVDA"), return it.
- If no ticker or company is found, return "NONE".
- Output only the ticker symbol or "NONE".
"""
