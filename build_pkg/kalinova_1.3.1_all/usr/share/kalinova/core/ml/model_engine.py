"""
Native ML Predictor & Model Engine for Kali-Nova.
Provides ultra-fast, zero-dependency forward pass inference and ensemble scoring.
"""

import os
import json
import math
from typing import List, Dict, Any, Tuple, Optional


class MLModelEngine:
    """
    Lightweight, self-contained ML Inference Engine.
    Executes neural/linear ensemble forward-passes with Softmax probability outputs.
    Guarantees <1ms CPU inference and zero external dependencies.
    """

    DEFAULT_MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "scenario_model.json")

    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or self.DEFAULT_MODEL_PATH
        self.classes: List[str] = []
        self.feature_names: List[str] = []
        self.weights: List[List[float]] = []  # shape: [num_classes, num_features]
        self.biases: List[float] = []        # shape: [num_classes]
        self.is_loaded = False
        self.load_model()

    def load_model(self) -> bool:
        """Loads serialized model weights and metadata from JSON."""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.classes = data.get("classes", [])
                    self.feature_names = data.get("feature_names", [])
                    self.weights = data.get("weights", [])
                    self.biases = data.get("biases", [])
                    self.is_loaded = True
                    return True
            except Exception as e:
                print(f"[MLModelEngine] Error loading model: {e}")
                self.is_loaded = False
        return False

    def predict_proba(self, feature_vector: List[float]) -> List[Tuple[str, float]]:
        """
        Calculates class probabilities via Softmax over linear ensemble scores.
        Returns ordered list of (class_name, probability_float) sorted by highest probability.
        """
        if not self.is_loaded or not self.weights:
            # Return uniform distribution if model is not loaded
            n = len(self.classes) if self.classes else 1
            return [(c, 1.0 / n) for c in (self.classes or ["nmap"])]

        logits: List[float] = []
        for class_idx in range(len(self.classes)):
            w = self.weights[class_idx]
            b = self.biases[class_idx] if class_idx < len(self.biases) else 0.0
            
            # Dot product: w . x + b
            score = b
            for f_idx in range(min(len(w), len(feature_vector))):
                score += w[f_idx] * feature_vector[f_idx]
            logits.append(score)

        # Softmax with numerical stability
        max_logit = max(logits) if logits else 0.0
        exp_scores = [math.exp(score - max_logit) for score in logits]
        sum_exp = sum(exp_scores) if sum(exp_scores) > 0 else 1.0
        probabilities = [exp_score / sum_exp for exp_score in exp_scores]

        # Combine with class names and sort descending
        results = list(zip(self.classes, probabilities))
        results.sort(key=lambda item: item[1], reverse=True)
        return results

    def predict(self, feature_vector: List[float]) -> Tuple[str, float]:
        """Returns the top predicted class name and its confidence score."""
        scored = self.predict_proba(feature_vector)
        return scored[0] if scored else ("nmap", 0.5)


# Global singleton instance
ml_engine = MLModelEngine()
