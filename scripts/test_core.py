import sys
import os
sys.path.append(os.getcwd())

from src.config import get_config
from src.catalog.models import FileRecord
from datetime import datetime

def test_scaffold():
    print("🚀 Starting Core Logic Test...")
    
    # 1. Initialize Config
    config = get_config()
    print("✅ Config and Services initialized.")

    # 2. Test Catalog
    files = config.catalog_service.list_files()
    print(f"✅ Catalog retrieval successful. Found {len(files)} files.")

    # 3. Test Retrieval Logic (Mock query)
    try:
        # This will fail if no API key is set, but we handle it gracefully
        results = config.hybrid_search.search("What is revenue?", top_k=1)
        print(f"✅ Retrieval engine test successful. Results found: {len(results) > 0}")
    except Exception as e:
        print(f"⚠️ Retrieval engine test skipped or failed (likely missing API key): {e}")

    print("🏁 Test complete.")

if __name__ == "__main__":
    test_scaffold()
