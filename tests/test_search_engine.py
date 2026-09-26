import pytest
from unittest.mock import MagicMock, patch
from src.search_engine import TravelSearchEngine

@pytest.fixture(autouse=True)
def mock_config():
    with patch("src.config.Config") as MockConfig:
        MockConfig.AZURE_OPENAI_API_KEY = "fake-key"
        MockConfig.AZURE_OPENAI_ENDPOINT = "https://fake.openai.azure.com/"
        MockConfig.AZURE_OPENAI_DEPLOYMENT_NAME = "gpt-4o"
        MockConfig.AZURE_SEARCH_ENDPOINT = "https://fake.search.windows.net"
        MockConfig.AZURE_SEARCH_KEY = "fake-key"
        MockConfig.MLFLOW_TRACKING_URI = None
        yield MockConfig

class TestTravelSearchEngine:
    @patch("src.search_engine.GovernanceGate")
    @patch("src.search_engine.AzureChatOpenAI")
    @patch("src.search_engine.AzureOpenAIEmbeddings")
    @patch("src.search_engine.get_vector_store")
    def test_initialization(self, mock_store, mock_embed, mock_chat, mock_gate):
        engine = TravelSearchEngine()
        assert engine is not None

    @patch("src.search_engine.GovernanceGate")
    @patch("src.search_engine.AzureChatOpenAI")
    @patch("src.search_engine.AzureOpenAIEmbeddings")
    @patch("src.search_engine.get_vector_store")
    def test_synthesize_response_prompt_requires_direct_answer(self, mock_store, mock_embed, mock_chat, mock_gate):
        mock_gate.return_value.validate_output.return_value = {"passed": True, "violations": []}
        mock_llm = MagicMock()
        mock_chat.return_value = mock_llm
        mock_llm.invoke.return_value.content = "Refunds depend on fare rules and timing."

        engine = TravelSearchEngine()
        docs = [MagicMock(page_content="Refunds are eligible according to fare rules and refund timing.", metadata={"source": "policy.pdf"})]

        engine.synthesize_response(docs, "What is the refund policy?")

        prompt = mock_llm.invoke.call_args[0][0]
        assert "Answer the question directly" in prompt
        assert "first sentence" in prompt.lower()

    @patch("src.search_engine.mlflow")
    @patch("src.search_engine.AzureChatOpenAI")
    @patch("src.search_engine.AzureOpenAIEmbeddings")
    @patch("src.search_engine.get_vector_store")
    def test_search_by_text(self, mock_store, mock_embed, mock_chat, mock_mlflow):
        # Mock vector store
        mock_vector_store = MagicMock()
        mock_store.return_value = mock_vector_store
        mock_vector_store.similarity_search.return_value = [
            MagicMock(page_content="Baggage allowance is 23kg", metadata={"source": "policy.pdf"})
        ]

        mock_mlflow.start_run.return_value.__enter__.return_value = None
        
        # Mock governance gate
        with patch("src.search_engine.GovernanceGate") as MockGate:
            mock_gate_instance = MagicMock()
            MockGate.return_value = mock_gate_instance
            mock_gate_instance.validate_input.return_value = {"passed": True, "violations": []}
            
            engine = TravelSearchEngine()
            results, query = engine.search_by_text("baggage rules", k=3)
            
            assert len(results) > 0
            assert query == "baggage rules"

    def test_fallback_relevancy_handles_synonyms(self):
        from src.evaluate import TravelChatbotEvaluator

        evaluator = TravelChatbotEvaluator.__new__(TravelChatbotEvaluator)
        dataset = {
            "question": ["What is the refund policy?"],
            "answer": ["Refund eligibility depends on the ticket fare and the applicable refund timing."],
            "contexts": [["The refund policy allows refunds based on fare conditions and timing requirements."]],
            "ground_truth": ["Refunds depend on fare conditions and timing."]
        }

        scores = evaluator._fallback_metrics(dataset)
        assert scores["answer_relevancy"] > 0.4

    @patch("src.search_engine.GovernanceGate")
    @patch("src.search_engine.AzureChatOpenAI")
    @patch("src.search_engine.AzureOpenAIEmbeddings")
    @patch("src.search_engine.get_vector_store")
    def test_select_relevant_docs_prefers_best_match(self, mock_store, mock_embed, mock_chat, mock_gate):
        engine = TravelSearchEngine()

        docs = [
            MagicMock(page_content="Weather delays can lead to rescheduling and rebooking options.", metadata={"source": "weather.pdf"}),
            MagicMock(page_content="Refunds must be issued within 7 days under DOT rules for credit-card purchases.", metadata={"source": "refund_policy.pdf"}),
        ]

        selected = engine._select_relevant_docs(docs, "How many days until the refund is issued?")

        assert selected[0].metadata["source"] == "refund_policy.pdf"

