import os
import hashlib
from typing import Tuple

class FileStorage:
    """Handles saving and reading raw files from the local filesystem."""
    def __init__(self, base_path: str = "data/uploads"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def save_file(self, filename: str, content: bytes) -> Tuple[str, str]:
        """
        Saves a file to the upload directory.
        Returns (file_path, file_hash).
        """
        file_hash = hashlib.md5(content).hexdigest()
        
        # Check if file with same hash already exists to avoid duplicates
        # In a real app, we might want to check the DB instead, but this is a helper.
        
        file_path = os.path.join(self.base_path, filename)
        
        # If file exists, we might want to append hash or handle naming
        if os.path.exists(file_path):
            name, ext = os.path.splitext(filename)
            file_path = os.path.join(self.base_path, f"{name}_{file_hash[:8]}{ext}")

        with open(file_path, "wb") as f:
            f.write(content)
            
        return file_path, file_hash

    def delete_file(self, file_path: str):
        """Deletes a file from the filesystem."""
        if os.path.exists(file_path):
            os.remove(file_path)
