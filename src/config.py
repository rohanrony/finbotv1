import os
from dotenv import load_dotenv
load_dotenv()
from src.storage.sqlite import SQLiteManager
from src.storage.files import FileStorage
from src.catalog.repository import CatalogRepository
from src.catalog.service import CatalogService
from src.ingestion.pipeline import IngestionPipeline
from src.retrieval.embeddings import EmbeddingProvider
from src.retrieval.vector_store import VectorStore
from src.retrieval.keyword_index import KeywordIndex
from src.retrieval.hybrid_search import HybridSearchEngine
from src.retrieval.context_builder import ContextBuilder
from src.llm.llm_client import LLMClient
from src.llm.engine import ChatbotEngine
from src.llm.answer_formatter import AnswerFormatter
from src.integrations.financial_datasets_client import FinancialDatasetsClient

class AppConfig:
    """Central configuration and service provider."""
    def __init__(self):
        self.db_path = "data/app.db"
        self.upload_path = "data/uploads"
        
        # Ensure directories exist
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        os.makedirs(self.upload_path, exist_ok=True)
        
        # Initialize Services
        self.db_manager = SQLiteManager(self.db_path)
        self.file_storage = FileStorage(self.upload_path)
        
        self.catalog_repo = CatalogRepository(self.db_manager)
        self.catalog_service = CatalogService(self.catalog_repo, self.file_storage)
        
        self.embedding_provider = EmbeddingProvider()
        self.vector_store = VectorStore("data/vectors")
        self.keyword_index = KeywordIndex(self.db_manager)
        self.hybrid_search = HybridSearchEngine(
            self.embedding_provider, 
            self.vector_store, 
            self.keyword_index
        )
        self.context_builder = ContextBuilder()
        
        self.llm_client = LLMClient()
        self.answer_formatter = AnswerFormatter()
        self.financial_datasets = FinancialDatasetsClient()
        self.chatbot_engine = ChatbotEngine(
            self.llm_client,
            self.hybrid_search,
            self.context_builder,
            self.financial_datasets
        )
        
        self.ingestion_pipeline = IngestionPipeline(self.db_manager, self.embedding_provider, self.vector_store)

# Singleton instance
_config = None

def get_config():
    global _config
    if _config is None:
        _config = AppConfig()
    return _config
