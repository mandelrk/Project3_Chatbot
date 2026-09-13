# import pytest
# from unittest.mock import MagicMock, patch
# from src.search_engine import TravelSearchEngine

# @pytest.fixture(autouse=True)
# def mock_config():
#     with patch("src.config.Config") as MockConfig:
#         MockConfig.AZURE_OPENAI_API_KEY = "fake-key"
#         MockConfig.AZURE_OPENAI_ENDPOINT = "https://fake.openai.azure.com/"
#         MockConfig.AZURE_OPENAI_DEPLOYMENT_NAME = "gpt-4o"
#         MockConfig.AZURE_SEARCH_ENDPOINT = "https://fake.search.windows.net"
#         MockConfig.AZURE_SEARCH_KEY = "fake-key"
#         MockConfig.MLFLOW_TRACKING_URI = None
#         yield MockConfig

# class TestTravelSearchEngine:
#     @patch("src.search_engine.AzureChatOpenAI")
#     @patch("src.search_engine.AzureOpenAIEmbeddings")
#     @patch("src.search_engine.get_vector_store")
#     def test_initialization(self, mock_store, mock_embed, mock_chat):
#         engine = TravelSearchEngine()
#         assert engine is not None

#     @patch("src.search_engine.AzureChatOpenAI")
#     @patch("src.search_engine.AzureOpenAIEmbeddings")
#     @patch("src.search_engine.get_vector_store")
#     def test_search_by_text(self, mock_store, mock_embed, mock_chat):
#         # Mock vector store
#         mock_vector_store = MagicMock()
#         mock_store.return_value = mock_vector_store
#         mock_vector_store.similarity_search.return_value = [
#             MagicMock(page_content="Baggage allowance is 23kg", metadata={"source": "policy.pdf"})
#         ]
        
#         # Mock governance gate
#         with patch("src.search_engine.GovernanceGate") as MockGate:
#             mock_gate_instance = MagicMock()
#             MockGate.return_value = mock_gate_instance
#             mock_gate_instance.validate_input.return_value = {"passed": True, "violations": []}
            
#             engine = TravelSearchEngine()
#             results, query = engine.search_by_text("baggage rules", k=3)
            
#             assert len(results) > 0
#             assert query == "baggage rules"

import pytest
from unittest.mock import MagicMock, patch
from src.search_engine import TravelSearchEngine

@pytest.fixture(autouse=True)
def mock_config():
    with patch("src.search_engine.Config") as MockConfig:
        # Azure OpenAI credentials & endpoints
        MockConfig.AZURE_OPENAI_API_KEY = "fake-openai-key"
        MockConfig.AZURE_OPENAI_ENDPOINT = "https://msft-ravi-june.cognitiveservices.azure.com/"
        MockConfig.AZURE_OPENAI_API_VERSION = "2024-12-01-preview"
        
        # Model deployment mappings
        MockConfig.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME = "gpt-5-mini"
        MockConfig.AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME = "text-embedding-3-small"
        
        # Azure AI Search configurations
        MockConfig.AZURE_SEARCH_SERVICE_ENDPOINT = "https://aisearchmand.search.windows.net"
        MockConfig.AZURE_SEARCH_API_KEY = "fake-search-key"
        MockConfig.AZURE_SEARCH_INDEX_NAME = "wandernest-travel-index"
        
        # MLflow configurations
        MockConfig.MLFLOW_TRACKING_URI = "http://localhost:5000"
        MockConfig.MLFLOW_EXPERIMENT_NAME = "travel-search-rag"
        yield MockConfig

class TestTravelSearchEngine:
    @patch("src.search_engine.AzureChatOpenAI")
    @patch("src.search_engine.AzureOpenAIEmbeddings")
    @patch("src.search_engine.get_vector_store")
    def test_initialization(self, mock_store, mock_embed, mock_chat):
        engine = TravelSearchEngine()
        assert engine is not None

    @patch("src.search_engine.AzureChatOpenAI")
    @patch("src.search_engine.AzureOpenAIEmbeddings")
    @patch("src.search_engine.get_vector_store")
    def test_search_by_text(self, mock_store, mock_embed, mock_chat):
        # Mock vector store similarity search output
        mock_vector_store = MagicMock()
        mock_store.return_value = mock_vector_store
        mock_vector_store.similarity_search.return_value = [
            MagicMock(page_content="Baggage allowance is 23kg", metadata={"source": "policy.pdf"})
        ]
        
        # Mock governance gate input validation
        with patch("src.search_engine.GovernanceGate") as MockGate:
            mock_gate_instance = MagicMock()
            MockGate.return_value = mock_gate_instance
            mock_gate_instance.validate_input.return_value = {"passed": True, "violations": []}
            
            engine = TravelSearchEngine()
            results, query = engine.search_by_text("baggage rules", k=3)
            
            assert len(results) > 0
            assert query == "baggage rules"
            mock_vector_store.similarity_search.assert_called_once_with("baggage rules", k=3)