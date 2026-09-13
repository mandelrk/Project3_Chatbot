"""
Ragas Evaluation for Travel Chatbot
RUBRIC: Evaluation Framework (RAGAS) (8 marks total)
- RAGAS evaluation implemented (3 marks)
- Golden dataset created (2 marks)
- All four metrics computed (2 marks)
- Results saved with pass/fail logic (1 mark)

TASK: Implement Ragas evaluation with 4 metrics
"""
import os
import json
import logging
import asyncio
import pandas as pd
from pathlib import Path
from typing import List, Dict

from src.search_engine import TravelSearchEngine
from src.config import Config

# HINT: Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("evaluation")


class TravelChatbotEvaluator:
    """Evaluates Travel Chatbot using Ragas metrics"""
    
    def __init__(self):
        # HINT: Initialize search engine and golden dataset path
        self.engine = TravelSearchEngine()
        self.golden_dataset_path = Path("data") / "golden_dataset.json"
    
    def load_golden_dataset(self) -> List[Dict]:
        """
        Load golden dataset for evaluation
        
        HINT: Check if file exists, if not create sample dataset
        """
        if not self.golden_dataset_path.exists():
            logger.warning(f"Golden dataset not found at {self.golden_dataset_path}")
            logger.info("Creating sample golden dataset...")
            return self._create_sample_dataset()
        
        with open(self.golden_dataset_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def _create_sample_dataset(self) -> List[Dict]:
        """
        Create sample golden dataset if not exists
        
        HINT: Create list of dicts with 'question' and 'ground_truth' keys
        Save to golden_dataset_path
        """
        sample_data = [
            {
                "question": "What are the baggage allowance rules for international flights?",
                "ground_truth": "The baggage allowance depends on the route and fare; consult the applicable airline policy."
            },
            {
                "question": "What is Air India's cancellation policy?",
                "ground_truth": "Cancellation charges and refund eligibility depend on the fare and applicable Air India policy."
            },
            {
                "question": "Do I need a visa to travel from India to UK?",
                "ground_truth": "Visa requirements depend on the traveler's nationality, destination, and immigration rules."
            },
            {
                "question": "What are the refund policies for flight cancellations?",
                "ground_truth": "Refund eligibility and timing depend on the cancellation reason, fare conditions, and applicable regulations."
            },
            {
                "question": "What documents do I need for international travel?",
                "ground_truth": "International travel commonly requires a valid passport and any visa or entry documents required by the destination."
            }
        ]
        
        # HINT: Save sample dataset
        self.golden_dataset_path.parent.mkdir(exist_ok=True)
        with open(self.golden_dataset_path, "w", encoding="utf-8") as f:
            json.dump(sample_data, f, indent=2)
        
        logger.info(f"Sample golden dataset saved to {self.golden_dataset_path}")
        return sample_data
    
    def generate_responses(self, questions: List[str]) -> tuple:
        """
        Generate responses for questions
        
        HINT: For each question:
        1. Search for documents
        2. Synthesize response
        3. Collect contexts
        Return (answers, contexts)
        """
        answers = []
        contexts = []
        
        for question in questions:
            logger.info(f"Generating answer for: {question}")
            
            try:
                # HINT: Search for relevant documents
                docs, _ = self.engine.search_by_text(question, k=5)
                
                # HINT: Generate answer
                answer = self.engine.synthesize_response(docs, question)
                
                # HINT: Collect contexts (retrieved documents)
                context_texts = [doc.page_content for doc in docs]
                
                answers.append(answer)
                contexts.append(context_texts)
                
            except Exception as e:
                logger.error(f"Error generating answer for '{question}': {e}")
                answers.append("Unable to generate an answer.")
                contexts.append([])
        
        return answers, contexts
    
    async def run_ragas_evaluation(self):
        """
        Run Ragas evaluation
        
        HINT: This method should:
        1. Load golden dataset
        2. Generate responses
        3. Prepare dataset dict
        4. Run Ragas evaluation with 4 metrics
        5. Save results
        """
        logger.info("=" * 70)
        logger.info("Starting Ragas Evaluation...")
        logger.info("=" * 70)

        try:
            from datasets import Dataset
            from ragas import evaluate
            from ragas.metrics import (
                answer_relevancy,
                context_precision,
                context_recall,
                faithfulness,
            )
        except ImportError as error:
            logger.error("RAGAS dependencies are unavailable: %s", error)
            return None
        
        # HINT: Load golden dataset
        golden_data = self.load_golden_dataset()
        
        if not golden_data:
            logger.error("No evaluation data available")
            return None
        
        logger.info(f"Loaded {len(golden_data)} test cases")
        
        # HINT: Extract questions and ground truths
        questions = [item["question"] for item in golden_data]
        ground_truths = [item["ground_truth"] for item in golden_data]
        
        # HINT: Generate answers and contexts
        logger.info("\nGenerating responses...")
        answers, contexts = self.generate_responses(questions)
        
        # HINT: Prepare dataset for Ragas
        dataset_dict = {
            "question": questions,
            "answer": answers,
            "contexts": contexts,
            "ground_truth": ground_truths
        }
        
        # HINT: Create HuggingFace Dataset
        hf_dataset = Dataset.from_dict(dataset_dict)
        
        logger.info("\nRunning Ragas metrics...")
        logger.info("Metrics: faithfulness, answer_relevancy, context_precision, context_recall")
        
        # HINT: Run evaluation
        try:
            results = evaluate(
                hf_dataset,
                metrics=[
                    faithfulness,
                    answer_relevancy,
                    context_precision,
                    context_recall
                ],
            )
            
            logger.info("\n" + "=" * 70)
            logger.info("EVALUATION RESULTS")
            logger.info("=" * 70)
            logger.info(f"\nRagas Scores:")
            logger.info(f"  Faithfulness:       {results['faithfulness']:.4f}")
            logger.info(f"  Answer Relevancy:   {results['answer_relevancy']:.4f}")
            logger.info(f"  Context Precision:  {results['context_precision']:.4f}")
            logger.info(f"  Context Recall:     {results['context_recall']:.4f}")
            logger.info("=" * 70)
            
            # HINT: Save detailed results
            self._save_results(results, dataset_dict)
            
            return results
            
        except Exception as e:
            logger.error(f"Ragas evaluation failed: {e}")
            logger.error("Make sure you have OPENAI_API_KEY set for Ragas to work")
            return None
    
    def _save_results(self, results: dict, dataset_dict: dict):
        """
        Save evaluation results to file
        
        HINT: Save summary JSON and detailed CSV
        """
        output_dir = Path("reports")
        output_dir.mkdir(exist_ok=True)

        thresholds = {
            "faithfulness": 0.70,
            "answer_relevancy": 0.70,
            "context_precision": 0.70,
            "context_recall": 0.70,
        }
        scores = {
            metric: float(results.get(metric, 0.0))
            for metric in thresholds
        }
        passed = all(scores[metric] >= threshold for metric, threshold in thresholds.items())
        
        # HINT: Save summary
        summary = {
            **scores,
            "thresholds": thresholds,
            "passed": passed,
            "total_test_cases": len(dataset_dict["question"])
        }
        
        summary_path = output_dir / "evaluation_summary.json"
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"\n✅ Evaluation summary saved to {summary_path}")
        
        # HINT: Save detailed results
        detailed_df = pd.DataFrame(dataset_dict)
        detailed_path = output_dir / "evaluation_detailed.csv"
        detailed_df.to_csv(detailed_path, index=False)
        
        logger.info(f"✅ Detailed results saved to {detailed_path}")
    
    def run(self):
        """Run evaluation (sync wrapper)"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.run_ragas_evaluation())
        finally:
            loop.close()


def run_evaluation():
    """
    Main evaluation function
    
    HINT: Run evaluator and check if results pass thresholds
    """
    evaluator = TravelChatbotEvaluator()
    results = evaluator.run()
    
    if results:
        # HINT: Check if evaluation passes minimum thresholds
        min_faithfulness = 0.70
        min_relevancy = 0.70
        
        passed = (
            results.get('faithfulness', 0) >= min_faithfulness and
            results.get('answer_relevancy', 0) >= min_relevancy
        )
        
        if passed:
            logger.info("\n✅ EVALUATION PASSED")
            return 0
        else:
            logger.warning("\n⚠️  EVALUATION BELOW THRESHOLDS")
            return 1
    else:
        logger.error("\n❌ EVALUATION FAILED")
        return 1


if __name__ == "__main__":
    import sys
    exit_code = run_evaluation()
    sys.exit(exit_code)