"""
Predictor — ML model loading and next-tool prediction.

Loads a pre-trained scikit-learn model and predicts which
tool the user should run next based on scan results.
"""

import os
import logging
from dataclasses import dataclass
from typing import List, Optional, Dict

logger = logging.getLogger(__name__)


@dataclass
class Prediction:
    """ML prediction result."""
    recommended_tool: str
    confidence: float  # 0.0 - 1.0
    confidence_label: str  # "high", "medium", "low"
    reasoning: str
    features_used: Dict[str, float]


class Predictor:
    """
    ML prediction engine for next-tool suggestions.

    Uses a pre-trained scikit-learn model (Decision Tree / Random Forest)
    to predict the most useful next tool based on current scan results.
    """

    # Label mapping: index → tool name
    LABEL_MAP = {
        0: "nikto",
        1: "hydra",
        2: "john",
        3: "dirb",
    }

    # Feature order expected by the model
    NMAP_FEATURE_ORDER = [
        "open_ports", "closed_ports", "filtered_ports",
        "http_detected", "https_detected", "ssh_detected",
        "ftp_detected", "smb_detected", "rdp_detected",
        "dns_detected", "telnet_detected", "mysql_detected",
        "total_services", "has_web_server", "has_auth_service",
    ]

    NIKTO_FEATURE_ORDER = [
        "total_vulns", "high_severity_count", "medium_severity_count",
        "low_severity_count", "has_directory_listing", "has_default_files",
        "has_outdated_server", "has_misconfig", "server_type",
    ]

    def __init__(self, model_path: str = ""):
        self._model = None
        self._model_path = model_path
        self._model_loaded = False

    def load_model(self, model_path: str = "") -> bool:
        """
        Load the pre-trained model from a .pkl file.

        Args:
            model_path: Path to the .pkl model file.

        Returns:
            True if model loaded successfully, False otherwise.
        """
        path = model_path or self._model_path

        if not path or not os.path.exists(path):
            logger.warning(f"ML model not found at: {path}")
            logger.info("ML suggestions will use rule-based fallback.")
            self._model_loaded = False
            return False

        try:
            import joblib
            self._model = joblib.load(path)
            self._model_loaded = True
            logger.info(f"ML model loaded from: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load ML model: {e}")
            self._model_loaded = False
            return False

    def predict(self, features: Dict[str, float],
                tool_name: str = "nmap") -> Prediction:
        """
        Predict the next recommended tool.

        Falls back to rule-based prediction if no ML model is loaded.

        Args:
            features: Feature dictionary from FeatureExtractor.
            tool_name: Source tool name (for feature ordering).

        Returns:
            Prediction object with tool recommendation and confidence.
        """
        if not features:
            return Prediction(
                recommended_tool="",
                confidence=0.0,
                confidence_label="low",
                reasoning="Insufficient data for prediction.",
                features_used=features,
            )

        if self._model_loaded and self._model is not None:
            return self._ml_predict(features, tool_name)
        else:
            return self._rule_based_predict(features, tool_name)

    def get_suggestions(self, features: Dict[str, float],
                        tool_name: str = "nmap",
                        top_n: int = 2) -> List[Prediction]:
        """
        Get top N tool suggestions with confidence scores.

        Args:
            features: Feature dictionary.
            tool_name: Source tool name.
            top_n: Number of suggestions to return.

        Returns:
            List of Prediction objects, sorted by confidence.
        """
        if self._model_loaded and self._model is not None:
            return self._ml_top_predictions(features, tool_name, top_n)
        else:
            # Rule-based returns single prediction
            return [self._rule_based_predict(features, tool_name)]

    def _ml_predict(self, features: Dict[str, float],
                    tool_name: str) -> Prediction:
        """Use trained ML model for prediction."""
        try:
            feature_vector = self._features_to_vector(features, tool_name)
            prediction_idx = self._model.predict([feature_vector])[0]
            probabilities = self._model.predict_proba([feature_vector])[0]
            confidence = float(max(probabilities))

            recommended = self.LABEL_MAP.get(prediction_idx, "unknown")
            confidence_label = self._confidence_label(confidence)

            return Prediction(
                recommended_tool=recommended,
                confidence=confidence,
                confidence_label=confidence_label,
                reasoning=self._generate_reasoning(recommended, features),
                features_used=features,
            )
        except Exception as e:
            logger.error(f"ML prediction failed: {e}. Using rule-based fallback.")
            return self._rule_based_predict(features, tool_name)

    def _ml_top_predictions(self, features: Dict[str, float],
                            tool_name: str,
                            top_n: int) -> List[Prediction]:
        """Get top N ML predictions."""
        try:
            feature_vector = self._features_to_vector(features, tool_name)
            probabilities = self._model.predict_proba([feature_vector])[0]

            # Get top N indices sorted by probability
            top_indices = sorted(
                range(len(probabilities)),
                key=lambda i: probabilities[i],
                reverse=True
            )[:top_n]

            predictions = []
            for idx in top_indices:
                recommended = self.LABEL_MAP.get(idx, "unknown")
                confidence = float(probabilities[idx])

                predictions.append(Prediction(
                    recommended_tool=recommended,
                    confidence=confidence,
                    confidence_label=self._confidence_label(confidence),
                    reasoning=self._generate_reasoning(recommended, features),
                    features_used=features,
                ))

            return predictions
        except Exception as e:
            logger.error(f"ML top predictions failed: {e}")
            return [self._rule_based_predict(features, tool_name)]

    def _rule_based_predict(self, features: Dict[str, float],
                            tool_name: str) -> Prediction:
        """
        Rule-based fallback when no ML model is available.

        Uses simple heuristics based on detected services.
        """
        has_web = features.get("has_web_server", 0) > 0
        has_http = features.get("http_detected", 0) > 0
        has_auth = features.get("has_auth_service", 0) > 0
        has_ssh = features.get("ssh_detected", 0) > 0
        has_ftp = features.get("ftp_detected", 0) > 0
        total_vulns = features.get("total_vulns", 0)
        high_vulns = features.get("high_severity_count", 0)

        recommended = ""
        confidence = 0.0
        reasoning = ""

        if tool_name == "nmap":
            # After Nmap, recommend based on what was found
            if has_web or has_http:
                recommended = "nikto"
                confidence = 0.85
                reasoning = (
                    "Web server detected (HTTP/HTTPS ports open). "
                    "Nikto can scan for web vulnerabilities."
                )
            elif has_ssh or has_ftp:
                recommended = "hydra"
                confidence = 0.75
                reasoning = (
                    "Authentication service detected (SSH/FTP). "
                    "Hydra can test for weak login credentials."
                )
            elif has_auth:
                recommended = "hydra"
                confidence = 0.65
                reasoning = (
                    "Authentication services found. "
                    "Consider testing login strength with Hydra."
                )
            else:
                recommended = "nikto"
                confidence = 0.40
                reasoning = (
                    "No specific services strongly indicate a next tool. "
                    "Nikto is suggested as a general follow-up."
                )

        elif tool_name == "nikto":
            # After Nikto, recommend based on vulnerability types
            if high_vulns > 0:
                recommended = "hydra"
                confidence = 0.70
                reasoning = (
                    "High severity vulnerabilities found. "
                    "Consider testing authentication if login forms were detected."
                )
            elif total_vulns > 5:
                recommended = "dirb"
                confidence = 0.65
                reasoning = (
                    "Multiple vulnerabilities found. "
                    "Dirb can discover hidden directories and files."
                )
            else:
                recommended = "dirb"
                confidence = 0.50
                reasoning = (
                    "Web scan completed. Directory brute-forcing with Dirb "
                    "may reveal additional attack surface."
                )

        if not recommended:
            recommended = "nikto"
            confidence = 0.30
            reasoning = "General recommendation — run a web vulnerability scan."

        return Prediction(
            recommended_tool=recommended,
            confidence=confidence,
            confidence_label=self._confidence_label(confidence),
            reasoning=reasoning,
            features_used=features,
        )

    def _features_to_vector(self, features: Dict[str, float],
                            tool_name: str) -> list:
        """Convert feature dict to ordered numeric list for ML model."""
        if tool_name == "nmap":
            order = self.NMAP_FEATURE_ORDER
        elif tool_name == "nikto":
            order = self.NIKTO_FEATURE_ORDER
        else:
            order = sorted(features.keys())

        return [features.get(f, 0.0) for f in order]

    @staticmethod
    def _confidence_label(confidence: float) -> str:
        """Map confidence score to label."""
        if confidence >= 0.75:
            return "high"
        elif confidence >= 0.50:
            return "medium"
        return "low"

    @staticmethod
    def _generate_reasoning(tool: str, features: Dict[str, float]) -> str:
        """Generate context-aware reasoning for a recommendation."""
        reasons = {
            "nikto": "Web server detected — Nikto will scan for web vulnerabilities.",
            "hydra": "Authentication services found — Hydra can test login security.",
            "john": "Authentication services found — John can crack captured hashes.",
            "dirb": "Web server detected — Dirb will discover hidden directories.",
        }
        return reasons.get(tool, f"Recommended tool: {tool}")

    @property
    def is_model_loaded(self) -> bool:
        """Check if ML model is loaded."""
        return self._model_loaded
