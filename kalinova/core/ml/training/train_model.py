"""
Training script for Kali-Nova ML Next-Step Scenario Predictor.
Trains a Softmax Ensemble Classifier and exports lightweight JSON weights for zero-dependency runtime inference.
"""

import os
import json
import random
from typing import List, Dict, Any
from core.ml.feature_extractor import FeatureExtractor
from core.ml.training.generate_dataset import generate_synthetic_scenarios


class AppStateStub:
    """Stub to emulate AppState during batch feature extraction."""
    def __init__(self, sample: Dict[str, Any]):
        self.open_ports = sample.get("open_ports", [])
        self.events = sample.get("events", [])
        self.last_tool_executed = sample.get("last_tool", "none")
        self.risk_score = sample.get("risk_score", 0)
        self.global_risk = sample.get("global_risk", "LOW")
        self.pipeline_artifacts = {
            "web_urls": ["http://target.com"] if sample.get("has_web_urls") else [],
            "fuzzed_endpoints": ["/login.php?id=1"] if sample.get("has_fuzzed_endpoints") else [],
            "hashes": ["5f4dcc3b5aa765d61d8327deb882cf99"] if sample.get("has_hashes") else []
        }


def train_and_export():
    """Generates dataset, trains multi-class softmax model via gradient descent, and saves weights."""
    print("[1/4] Generating synthetic penetration testing scenarios...")
    dataset = generate_synthetic_scenarios(count=6000)

    classes = FeatureExtractor.CLASSES
    class_to_idx = {c: i for i, c in enumerate(classes)}
    feature_names = FeatureExtractor.get_feature_names()
    num_features = len(feature_names)
    num_classes = len(classes)

    print(f"[2/4] Extracting {num_features} features across {len(dataset)} samples for {num_classes} classes...")
    X = []
    y = []

    for item in dataset:
        stub = AppStateStub(item)
        feat = FeatureExtractor.extract_features(stub)
        target_label = item.get("target_action", "nmap")
        if target_label in class_to_idx:
            X.append(feat)
            y.append(class_to_idx[target_label])

    # Initialize weights and biases
    weights = [[0.0 for _ in range(num_features)] for _ in range(num_classes)]
    biases = [0.0 for _ in range(num_classes)]

    # Softmax Logistic Regression / Gradient Descent Training
    lr = 0.08
    epochs = 45
    print(f"[3/4] Training Softmax Ensemble for {epochs} epochs...")

    for epoch in range(epochs):
        indices = list(range(len(X)))
        random.shuffle(indices)
        correct = 0

        for idx in indices:
            x_vec = X[idx]
            target_class = y[idx]

            # Compute logits
            logits = []
            for c_idx in range(num_classes):
                score = biases[c_idx]
                w = weights[c_idx]
                for f_idx in range(num_features):
                    score += w[f_idx] * x_vec[f_idx]
                logits.append(score)

            # Softmax
            max_l = max(logits)
            exp_scores = [pow(2.718281828459045, s - max_l) for s in logits]
            sum_exp = sum(exp_scores)
            probs = [s / sum_exp for s in exp_scores]

            # Track accuracy
            pred_class = probs.index(max(probs))
            if pred_class == target_class:
                correct += 1

            # Backpropagation / Gradient Step: dL/dz = prob - y_true
            for c_idx in range(num_classes):
                grad = probs[c_idx] - (1.0 if c_idx == target_class else 0.0)
                biases[c_idx] -= lr * grad
                for f_idx in range(num_features):
                    if x_vec[f_idx] != 0:
                        weights[c_idx][f_idx] -= lr * grad * x_vec[f_idx]

        train_acc = (correct / len(X)) * 100.0
        if (epoch + 1) % 10 == 0 or epoch == epochs - 1:
            print(f"  Epoch {epoch+1:02d}/{epochs:02d} - Training Accuracy: {train_acc:.2f}%")

    # Output directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
    os.makedirs(output_dir, exist_ok=True)
    model_file = os.path.join(output_dir, "scenario_model.json")

    model_payload = {
        "model_type": "SoftmaxEnsemble",
        "classes": classes,
        "feature_names": feature_names,
        "weights": weights,
        "biases": biases,
        "metadata": {
            "training_samples": len(X),
            "epochs": epochs,
            "final_accuracy": f"{train_acc:.2f}%",
            "framework": "Kali-Nova-ML-Native"
        }
    }

    with open(model_file, "w", encoding="utf-8") as f:
        json.dump(model_payload, f, indent=2)

    print(f"[4/4] Model serialized successfully to: {model_file}")
    return model_file


if __name__ == "__main__":
    train_and_export()
