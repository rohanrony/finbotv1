import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from src.app_state import init_session_state
from src.ui.chat_panel import render_chat_panel
from src.ui.upload_panel import render_upload_panel
from src.ui.library_panel import render_library_panel
from src.ui.settings_panel import render_settings_panel

# Page configuration
st.set_page_config(
    page_title="Financial Analyst Bot",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
init_session_state()

# Sidebar
with st.sidebar:
    st.title("📈 FinAnalyst Bot")
    st.markdown("---")
    st.info("MVP v1.0 - Analyze 10-K, 10-Q and S-1 filings.")
    
    if st.button("Reset Chat", use_container_width=True):
        from src.app_state import reset_chat
        reset_chat()
        st.rerun()

# Main UI
st.title("Financial Analyst Chatbot")

# Define Tabs
tab_chat, tab_ingestion, tab_library, tab_settings = st.tabs([
    "💬 Chat", 
    "📥 Ingestion", 
    "📚 Filing Library", 
    "⚙️ Settings"
])

with tab_chat:
    render_chat_panel()

with tab_ingestion:
    render_upload_panel()

with tab_library:
    render_library_panel()

with tab_settings:
    render_settings_panel()
