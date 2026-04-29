import streamlit as st
import pandas as pd
import json

class AnswerFormatter:
    """Formats LLM responses and associated data for Streamlit display."""
    
    def render_message(self, role: str, content: str, table_data: str = None):
        """Renders a message with optional table data."""
        with st.chat_message(role):
            st.markdown(content)
            if table_data:
                try:
                    df = pd.read_json(table_data, orient='records')
                    st.dataframe(df, use_container_width=True)
                except:
                    pass

    def format_citations(self, text: str) -> str:
        """Post-process text to highlight or format citations."""
        # For MVP, assume LLM follows instructions.
        return text
