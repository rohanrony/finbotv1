import streamlit as st
from datetime import datetime
from src.config import get_config

def render_upload_panel():
    """Renders the file upload and ingestion interface."""
    st.header("Document Ingestion")
    
    config = get_config()
    catalog_service = config.catalog_service
    ingestion_pipeline = config.ingestion_pipeline

    with st.form("upload_form", clear_on_submit=True):
        uploaded_files = st.file_uploader(
            "Upload SEC Filing (PDF)", 
            type=["pdf"], 
            accept_multiple_files=True
        )
        
        col1, col2 = st.columns(2)
        with col1:
            ticker = st.text_input("Ticker (e.g. AAPL)", help="Optional: Enter ticker symbol")
            filing_type = st.selectbox("Filing Type", ["10-K", "10-Q", "S-1", "Other"])
        
        with col2:
            year = st.number_input("Document Year", min_value=2000, max_value=2100, value=datetime.now().year)
            period = st.text_input("Period (e.g. Q3, Annual)", help="Optional: Enter fiscal period")

        submit_button = st.form_submit_button("Upload and Record")

    if submit_button and uploaded_files:
        metadata = {
            "ticker": ticker.upper() if ticker else None,
            "filing_type": filing_type,
            "document_year": year,
            "period_label": period
        }
        
        for uploaded_file in uploaded_files:
            content = uploaded_file.read()
            success, message = catalog_service.upload_file(uploaded_file.name, content, metadata)
            if success:
                st.success(message)
            else:
                st.error(message)
        
        st.rerun()

    st.divider()
    st.subheader("Filing Catalog Status")
    
    files = catalog_service.list_files()
    if not files:
        st.info("No files in the catalog. Upload a file above.")
    else:
        for file in files:
            cols = st.columns([3, 2, 2, 1])
            cols[0].write(file.filename)
            cols[1].write(file.filing_type)
            cols[2].write(file.status)
            
            # Action button
            if file.status == "Uploaded":
                if cols[3].button("Ingest", key=file.file_id):
                    with st.spinner(f"Ingesting {file.filename}..."):
                        success = ingestion_pipeline.process_file(file.file_id, file.file_path)
                        if success:
                            st.success(f"Ingested {file.filename}")
                        else:
                            st.error(f"Failed to ingest {file.filename}")
                        st.rerun()
            elif "Error" in file.status:
                if cols[3].button("Retry", key=file.file_id):
                    file.status = "Uploaded" # Reset status for retry
                    st.rerun()
            else:
                cols[3].write("✅")
