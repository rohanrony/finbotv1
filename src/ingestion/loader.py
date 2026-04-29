import pypdf
from typing import List

class DocumentLoader:
    """Handles loading and initial text extraction from PDF files."""
    def load_pdf(self, file_path: str) -> str:
        """
        Extract text from a PDF file.
        Returns the full text of the document.
        """
        text = ""
        try:
            with open(file_path, "rb") as f:
                reader = pypdf.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n\n"
        except Exception as e:
            print(f"Error loading PDF: {e}")
            raise e
        return text
