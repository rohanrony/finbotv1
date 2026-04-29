import streamlit as st
import pandas as pd
import json
from src.config import get_config

def render_library_panel():
    """Renders the filing library/catalog view with preview support."""
    st.header("Filing Library")
    
    config = get_config()
    catalog_service = config.catalog_service
    
    files = catalog_service.list_files()
    
    if not files:
        st.info("The library is empty. Go to 'Ingestion' to upload files.")
        return

    # 1. Search and Filter Controls
    col_s1, col_s2 = st.columns([2, 1])
    with col_s1:
        search_query = st.text_input("Search by filename or ticker...", placeholder="e.g. AAPL")
    with col_s2:
        type_filter = st.multiselect("Filing Type", ["10-K", "10-Q", "S-1"])

    # Prepare DataFrame
    data = [
        {
            "ID": f.file_id[:8], 
            "Filename": f.filename, 
            "Ticker": f.ticker or "N/A", 
            "Type": f.filing_type, 
            "Year": f.document_year, 
            "Status": f.status, 
            "Created": f.created_at.strftime("%Y-%m-%d %H:%M"),
            "original_id": f.file_id
        } 
        for f in files
    ]
    df = pd.DataFrame(data)
    
    # Apply filters
    if search_query:
        df = df[df['Filename'].str.contains(search_query, case=False) | df['Ticker'].str.contains(search_query, case=False)]
    if type_filter:
        df = df[df['Type'].isin(type_filter)]

    # Display Table
    st.dataframe(
        df.drop(columns=["original_id"]),
        use_container_width=True,
        hide_index=True
    )

    # 2. Detailed Inspection & Actions
    st.divider()
    st.subheader("Document Inspector")
    
    selected_filename = st.selectbox("Select a document to inspect", df["Filename"].tolist() if not df.empty else [])
    
    if selected_filename:
        file_id = df[df["Filename"] == selected_filename]["original_id"].values[0]
        file_status = df[df["Filename"] == selected_filename]["Status"].values[0]
        
        tab_meta, tab_text, tab_tables = st.tabs(["📋 Metadata", "📄 Text Preview", "📊 Table Preview"])
        
        with tab_meta:
            st.json(df[df["original_id"] == file_id].to_dict('records')[0])
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Re-ingest Document", help="Resets status to allow re-processing"):
                    catalog_service.reset_file_status(file_id)
                    st.success("Status reset. Go to 'Ingestion' to re-process.")
                    st.rerun()
            with c2:
                if st.button("Delete from Library", type="secondary"):
                    if catalog_service.delete_file(file_id):
                        st.warning(f"Deleted {selected_filename}")
                        st.rerun()

        with tab_text:
            if file_status != "Ingested":
                st.warning("Please ingest the document first to preview text chunks.")
            else:
                chunks = catalog_service.get_file_content_preview(file_id)
                if chunks:
                    for i, chunk in enumerate(chunks[:10]): # Show first 10 chunks
                        with st.expander(f"Chunk {i+1}: {chunk['heading'] or 'No Heading'}"):
                            st.write(chunk['chunk_text'])
                    if len(chunks) > 10:
                        st.caption(f"... and {len(chunks)-10} more chunks.")
                else:
                    st.info("No text chunks found for this document.")

        with tab_tables:
            if file_status != "Ingested":
                st.warning("Please ingest the document first to preview tables.")
            else:
                tables = catalog_service.get_file_tables(file_id)
                if tables:
                    for table in tables:
                        st.write(f"**{table['table_name']}**")
                        try:
                            table_df = pd.read_json(table["dataframe_json"], orient='records')
                            st.dataframe(table_df, use_container_width=True)
                        except:
                            st.error("Failed to render table.")
                else:
                    st.info("No tables extracted from this document.")
