import streamlit as st
import os
from src.config import get_config

def render_settings_panel():
    """Renders the application settings and OpenAI API key configuration."""
    st.header("Settings")
    
    config = get_config()

    st.subheader("API Configuration")
    with st.expander("API Keys", expanded=True):
        # 1. Check if keys are in environment
        env_openai = os.getenv("OPENAI_API_KEY", "")
        env_fin = os.getenv("FINANCIAL_DATASETS_API_KEY", "")

        # 2. Check if keys are in session state (user entered)
        session_openai = st.session_state.api_keys.get("openai", "")
        session_fin = st.session_state.api_keys.get("financial_datasets", "")

        # Labels to indicate status
        openai_label = "OpenAI API Key"
        if env_openai and not session_openai:
            openai_label += " (Set via Environment ✅)"
        elif session_openai:
            openai_label += " (Overriding Environment 🛠️)"

        fin_label = "Financial Datasets API Key"
        if env_fin and not session_fin:
            fin_label += " (Set via Environment ✅)"
        elif session_fin:
            fin_label += " (Overriding Environment 🛠️)"

        # 3. Render inputs (only show session_openai to hide env keys)
        openai_key = st.text_input(
            openai_label, 
            value=session_openai,
            type="password",
            help="Enter a key here to override the .env file."
        )
        fin_key = st.text_input(
            fin_label, 
            value=session_fin,
            type="password",
            help="Enter a key here to override the .env file."
        )
        
        if st.button("Save API Keys"):
            # Update session state
            st.session_state.api_keys["openai"] = openai_key
            st.session_state.api_keys["financial_datasets"] = fin_key
            
            # Determine which key to use for the services
            # User entry takes precedence over Env
            active_openai = openai_key or env_openai
            active_fin = fin_key or env_fin

            # Update the services in real-time
            config.llm_client.api_key = active_openai
            config.embedding_provider.api_key = active_openai
            config.financial_datasets.api_key = active_fin
            
            st.success("Configuration updated for the current session.")

    st.subheader("Model & Retrieval Settings")
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Default LLM Model", ["gpt-4o", "gpt-4o-mini"], index=0)
        st.slider("Top-K Semantic Results", min_value=1, max_value=20, value=5)
    
    with col2:
        st.toggle("Use Financial Datasets API", value=True)
        st.slider("Context Chunk Overlap", min_value=0, max_value=500, value=200)

    st.divider()
    st.subheader("About")
    st.markdown("""
    **Financial Analyst Bot v1.0**
    Built with Streamlit, SQLite, and OpenAI.
    
    *Analyze SEC filings with hybrid retrieval and intelligent reasoning.*
    """)
