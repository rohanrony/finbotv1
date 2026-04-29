# Financial Analyst Chatbot

A modular Streamlit application for analyzing SEC filings (10-K, 10-Q, S-1) using Google Gemini and the Financial Datasets API.

## Features
- **Intelligent Ingestion**: Automatically parses SEC filings into narrative sections and financial tables.
- **Hybrid Retrieval**: Combines semantic search (embeddings) with keyword matching for high-precision context.
- **Analyst Persona**: LLM is tuned to behave like a professional financial analyst.
- **External Data**: Integrates with Financial Datasets API for real-time numeric data analysis.
- **Rich UI**: Interactive chat, document library, and preview inspector.

## Setup

### 1. Prerequisites
- Python 3.9+
- An OpenAI API Key ([OpenAI](https://openai.com/))
- (Optional) A Financial Datasets API Key ([Financial Datasets](https://financialdatasets.ai/))

### 2. Installation
```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file from the example:
```bash
cp .env.example .env
```
Edit `.env` and add your `OPENAI_API_KEY` and `FINANCIAL_DATASETS_API_KEY`.

## Running the App
```bash
streamlit run app.py
```

## Project Structure
- `src/ui/`: Streamlit interface components.
- `src/catalog/`: Document management and metadata.
- `src/ingestion/`: PDF parsing and chunking pipeline.
- `src/retrieval/`: Semantic and keyword search logic.
- `src/llm/`: Gemini integration and prompt engineering.
- `src/integrations/`: External API clients.
- `src/storage/`: SQLite and filesystem persistence.

## Testing
Run the core logic test script:
```bash
python scripts/test_core.py
```

## Usage
1. Upload 10-K, 10-Q, or S-1 filings as PDF docs and ask questions specific to filing text. Upload multiple docs to compare them.
2. Ask questions related metrics in financial statements pulled in from financialdatasets.ai

