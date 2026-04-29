import streamlit as st
from src.config import get_config

def render_chat_panel():
    """Renders the main chat interface."""
    st.header("Chat with Filings")

    config = get_config()
    chatbot_engine = config.chatbot_engine
    answer_formatter = config.answer_formatter

    # Sidebar for chat settings
    with st.expander("Search Filters", expanded=False):
        ticker_filter = st.text_input("Filter by Ticker (optional)", placeholder="e.g. AAPL")
        filing_type_filter = st.multiselect("Filter by Filing Type", ["10-K", "10-Q", "S-1"])

    filters = {}
    if ticker_filter:
        filters["ticker"] = ticker_filter.upper()
    if filing_type_filter:
        filters["filing_type"] = filing_type_filter

    # Display chat history
    for message in st.session_state.messages:
        answer_formatter.render_message(
            message["role"], 
            message["content"], 
            message.get("table_data")
        )

    # Chat input
    if prompt := st.chat_input("Ask a question about your filings..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing filings and financial data..."):
                answer, search_results, table_json = chatbot_engine.ask(
                    prompt, 
                    st.session_state.messages,
                    filters=filters if filters else None
                )
                
                st.markdown(answer)
                
                # Render table if present
                if table_json:
                    import pandas as pd
                    try:
                        df = pd.read_json(table_json, orient='records')
                        st.dataframe(df, use_container_width=True)
                    except:
                        pass
                
                # Show source citations in an expander
                if search_results:
                    with st.expander("Sources Cited", expanded=False):
                        for res in search_results:
                            meta = res["metadata"]
                            st.write(f"**{meta.get('ticker', 'N/A')} {meta.get('filing_type', 'Document')}** - {meta.get('heading', 'Section')}")
                            st.caption(res["chunk_text"][:200] + "...")

        # Add assistant message to chat history
        st.session_state.messages.append({
            "role": "assistant", 
            "content": answer,
            "table_data": table_json,
            "sources": [res["metadata"] for res in search_results] if search_results else []
        })
