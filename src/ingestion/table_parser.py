import pdfplumber
import pandas as pd
from typing import List, Dict

class TableParser:
    """Extracts tables from PDFs and returns them as DataFrames."""
    
    def extract_tables(self, file_path: str) -> List[pd.DataFrame]:
        """
        Extract tables using pdfplumber.
        Returns a list of pandas DataFrames with unique columns.
        """
        dfs = []
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables:
                        if not table or len(table) < 2:
                            continue
                            
                        # Extract headers and handle duplicates/None
                        headers = table[0]
                        cleaned_headers = []
                        for i, h in enumerate(headers):
                            val = str(h).strip() if h else f"Col_{i}"
                            cleaned_headers.append(val)
                            
                        # Ensure uniqueness for JSON serialization
                        seen = {}
                        unique_headers = []
                        for h in cleaned_headers:
                            if h in seen:
                                seen[h] += 1
                                unique_headers.append(f"{h}_{seen[h]}")
                            else:
                                seen[h] = 0
                                unique_headers.append(h)

                        # Create DataFrame
                        df = pd.DataFrame(table[1:], columns=unique_headers)
                        df = df.dropna(how='all').dropna(axis=1, how='all')
                        
                        if not df.empty:
                            dfs.append(df)
        except Exception as e:
            print(f"Error extracting tables: {e}")
            
        return dfs
