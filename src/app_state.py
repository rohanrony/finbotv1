import streamlit as st

def init_session_state():
    """Initializes the Streamlit session state variables if they don't exist."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your Financial Analyst Bot. Upload some filings in the Ingestion tab to get started."}
        ]
    
    if "api_keys" not in st.session_state:
        st.session_state.api_keys = {
            "gemini": "",
            "financial_datasets": ""
        }
    
    if "file_catalog" not in st.session_state:
        st.session_state.file_catalog = []

    if "ingestion_status" not in st.session_state:
        st.session_state.ingestion_status = {}

    if "processing_queue" not in st.session_state:
        st.session_state.processing_queue = []

def reset_chat():
    """Resets the chat history in the session state."""
    st.session_state.messages = []
