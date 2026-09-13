"""
Configuration Management
RUBRIC: Environment Setup & Configuration (8 marks total)
- Azure OpenAI credentials configured correctly (1 mark)
- Azure AI Search credentials set up properly (1 mark)
- config.py implemented with validation (3 marks)
- All required packages installed and imported without errors (3 marks)

TASK: Load all configuration from environment variables
"""
# import os
# from dotenv import load_dotenv

# # HINT: Load environment variables from .env file
# ___()  # HINT: load_dotenv()

# class Config:
#     """Configuration for Wanderlust Travel Chatbot"""
    
#     # ====================
#     # Azure OpenAI Configuration
#     # ====================
#     # HINT: Load Azure OpenAI credentials from environment
#     AZURE_OPENAI_API_KEY = os.getenv("___") 
#     AZURE_OPENAI_ENDPOINT = os.getenv("___") 
#     AZURE_OPENAI_API_VERSION = os.getenv("___", "___")  
#     AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("___", "___")  
#     AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.getenv("___", "___") 
    
#     # ====================
#     # Azure AI Search Configuration (Only vector store - no ChromaDB)
#     # ====================
#     # HINT: Load Azure AI Search credentials
#     AZURE_SEARCH_ENDPOINT = os.getenv("___") 
#     AZURE_SEARCH_KEY = os.getenv("___") 
#     AZURE_SEARCH_INDEX_NAME = os.getenv("___", "___")  # HINT: "AZURE_SEARCH_INDEX_NAME", "travel-kb-index"
    
#     # ====================
#     # Azure Storage (Optional)
#     # ====================
#     AZURE_STORAGE_CONNECTION_STRING = os.getenv("___")  
#     AZURE_STORAGE_CONTAINER_NAME = os.getenv("___", "___")  # HINT: "AZURE_STORAGE_CONTAINER_NAME", "travel-documents"
    
#     # ====================
#     # Azure Content Safety (Optional)
#     # ====================
#     AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("___")  
#     AZURE_CONTENT_SAFETY_KEY = os.getenv("___") 
    
#     # ====================
#     # Azure Monitor (Optional)
#     # ====================
#     APPLICATIONINSIGHTS_CONNECTION_STRING = os.getenv("___") 
    
#     # ====================
#     # MLflow Configuration
#     # ====================
#     MLFLOW_TRACKING_URI = os.getenv("___")  # HINT: "MLFLOW_TRACKING_URI"
#     MLFLOW_EXPERIMENT_NAME = os.getenv("___", "___")  # HINT: "MLFLOW_EXPERIMENT_NAME", "wanderlust-travel-chatbot"
    
#     # ====================
#     # Ingestion Settings
#     # ====================
#     # HINT: Convert to integer, 0 means no limit
#     INGESTION_LIMIT = int(os.getenv("___", "___"))  # HINT: "INGESTION_LIMIT", "0"

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class with strict validation for Azure RAG Services."""

    # Azure OpenAI Configuration
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "").strip()
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "").strip()
    AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview").strip()
    AZURE_OPENAI_DEPLOYMENT_NAME: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4").strip()
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT: str = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small").strip()

    # Vector Store & Azure Search Configuration
    VECTOR_STORE_TYPE: str = os.getenv("VECTOR_STORE_TYPE", "azure_search").strip()
    AZURE_SEARCH_ENDPOINT: str = os.getenv("AZURE_SEARCH_ENDPOINT", "").strip()
    AZURE_SEARCH_KEY: str = os.getenv("AZURE_SEARCH_KEY", "").strip()
    AZURE_SEARCH_INDEX_NAME: str = os.getenv("AZURE_SEARCH_INDEX_NAME", "travel-search-index").strip()

    # Optional Monitoring & Safety Settings
    MLFLOW_TRACKING_URI: str = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000").strip()
    MLFLOW_EXPERIMENT_NAME: str = os.getenv("MLFLOW_EXPERIMENT_NAME", "travel-search-rag").strip()

    @classmethod
    def validate(cls) -> None:
        """Validates that all required environment variables are set and properly structured."""
        missing_vars = []

        if not cls.AZURE_OPENAI_API_KEY:
            missing_vars.append("AZURE_OPENAI_API_KEY")
        if not cls.AZURE_OPENAI_ENDPOINT:
            missing_vars.append("AZURE_OPENAI_ENDPOINT")
        elif not cls.AZURE_OPENAI_ENDPOINT.startswith("https://"):
            raise ValueError(f"Invalid AZURE_OPENAI_ENDPOINT: '{cls.AZURE_OPENAI_ENDPOINT}'. Must start with 'https://'.")

        if cls.VECTOR_STORE_TYPE == "azure_search":
            if not cls.AZURE_SEARCH_ENDPOINT:
                missing_vars.append("AZURE_SEARCH_ENDPOINT")
            elif not cls.AZURE_SEARCH_ENDPOINT.startswith("https://"):
                raise ValueError(f"Invalid AZURE_SEARCH_ENDPOINT: '{cls.AZURE_SEARCH_ENDPOINT}'. Must start with 'https://'.")

            if not cls.AZURE_SEARCH_KEY:
                missing_vars.append("AZURE_SEARCH_KEY")

        if missing_vars:
            raise ValueError(f"Missing required environment variables in configuration: {', '.join(missing_vars)}")

# Run validation on module import
Config.validate()