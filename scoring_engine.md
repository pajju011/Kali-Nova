# Kalinova — Scoring Engine Document

**Version:** 1.0 | **Date:** 2026-03-03

> **Scalability Note:** The scoring engine is designed to **scale its prediction targets** as new tools are added. The MVP predicts across 4 tools, but as the tool library grows towards 600+, the model will be retrained to recommend from an expanding set of tools.

---

## 1. Overview

The Kalinova Scoring Engine is the **ML Intelligence Layer** responsible for analyzing assessment tool results and producing intelligent next-step recommendations. It uses a trained classification model to predict which security tool the user should run next, along with a confidence score.

---

## 2. Scoring Engine Architecture

```
┌────────────────┐
│  Parsed Data   │  (from Parser Layer)
│  (structured)  │
└───────┬────────┘
        │
┌───────▼────────┐
│   Feature      │  Converts parsed results to
│   Extractor    │  numeric feature vector
└───────┬────────┘
        │
┌───────▼────────┐
│   Model        │  Loads pre-trained .pkl model
│   Loader       │  (Decision Tree / Random Forest)
└───────┬────────┘
        │
┌───────▼────────┐
│   Predictor    │  Runs inference
│                │  Returns tool + confidence
└───────┬────────┘
        │
┌───────▼────────┐
│  Confidence    │  Classifies confidence level
│  Scorer        │  High / Medium / Low
└───────┬────────┘
        │
┌───────▼────────┐
│  Suggestion    │  Formats output for UI
│  Formatter     │
└────────────────┘
```

---

## 3. Feature Extraction

### 3.1 Feature Set — Nmap Results

| Feature Name       | Type    | Derivation                            | Example |
|--------------------|---------|---------------------------------------|---------|
| `open_ports`       | Integer | Count of open ports                   | 5       |
| `closed_ports`     | Integer | Count of closed ports                 | 12      |
| `http_detected`    | Binary  | 1 if port 80 or 443 is open          | 1       |
| `ssh_detected`     | Binary  | 1 if port 22 is open                 | 1       |
| `ftp_detected`     | Binary  | 1 if port 21 is open                 | 0       |
| `smb_detected`     | Binary  | 1 if port 445 is open                | 0       |
| `rdp_detected`     | Binary  | 1 if port 3389 is open               | 0       |
| `dns_detected`     | Binary  | 1 if port 53 is open                 | 0       |
| `total_services`   | Integer | Total unique services identified      | 4       |
| `has_web_server`   | Binary  | 1 if HTTP/HTTPS service found         | 1       |
| `has_auth_service` | Binary  | 1 if SSH/FTP/RDP found               | 1       |
| `os_detected`      | Binary  | 1 if OS detection returned result     | 0       |

### 3.2 Feature Set — Nikto Results

| Feature Name           | Type    | Derivation                          | Example |
|------------------------|---------|-------------------------------------|---------|
| `total_vulns`          | Integer | Count of vulnerabilities found      | 8       |
| `high_severity_count`  | Integer | Count of high/critical findings     | 2       |
| `medium_severity_count`| Integer | Count of medium findings            | 3       |
| `low_severity_count`   | Integer | Count of low/info findings          | 3       |
| `has_directory_listing`| Binary  | 1 if directory listing found        | 1       |
| `has_default_files`    | Binary  | 1 if default files detected         | 0       |
| `has_outdated_server`  | Binary  | 1 if server version is outdated     | 1       |
| `has_misconfig`        | Binary  | 1 if misconfiguration detected      | 1       |
| `server_type`          | Encoded | Apache=1, Nginx=2, IIS=3, Other=0  | 1       |

### 3.3 Feature Extraction Code Contract

```python
class FeatureExtractor:
    def extract(self, tool_name: str, parsed_data: dict) -> dict:
        """Extract numeric feature vector from parsed tool output.
        
        Args:
            tool_name: "nmap" or "nikto"
            parsed_data: structured dict from parser
        Returns:
            dict of feature_name → numeric_value
        """
        if tool_name == "nmap":
            return self._extract_nmap_features(parsed_data)
        elif tool_name == "nikto":
            return self._extract_nikto_features(parsed_data)
        raise ValueError(f"Unsupported tool: {tool_name}")
```

---

## 4. ML Model Specification

### 4.1 Model Configuration

| Property               | Value                                     |
|------------------------|-------------------------------------------|
| **Algorithm**          | Random Forest Classifier (primary)        |
| **Fallback Algorithm** | Decision Tree Classifier                  |
| **Library**            | scikit-learn                              |
| **Serialization**      | joblib (.pkl format)                      |
| **Model Location**     | `/opt/kalinova/models/next_tool_model.pkl`|
| **Input**              | Numeric feature vector (12-15 features)   |
| **Output Labels**      | Tool names: "nikto", "hydra", "john", "dirb" |
| **Training Data**      | 500+ synthetic + real-world scan samples  |

### 4.2 Training Pipeline

```
Raw Scan Data → Feature Extraction → Label Assignment → Train/Test Split
                                                              │
                                                    ┌─────────▼──────────┐
                                                    │  Model Training    │
                                                    │  (Random Forest)   │
                                                    └─────────┬──────────┘
                                                              │
                                                    ┌─────────▼──────────┐
                                                    │  Evaluation        │
                                                    │  (accuracy, F1)    │
                                                    └─────────┬──────────┘
                                                              │
                                                    ┌─────────▼──────────┐
                                                    │  Export .pkl       │
                                                    │  (joblib.dump)     │
                                                    └────────────────────┘
```

### 4.3 Label Mapping (Prediction Targets)

| Label ID | Tool Name  | When Recommended                                         |
|----------|------------|----------------------------------------------------------|
| 0        | `nikto`    | Web server detected (HTTP/HTTPS open)                    |
| 1        | `hydra`    | Authentication services detected (SSH, FTP, RDP)         |
| 2        | `john`     | Authentication services detected + credential focus      |
| 3        | `dirb`     | Web server detected + directory listing interest         |
| ...      | *(future)* | New labels added as tools are integrated (sqlmap, enum4linux, gobuster, aircrack-ng, etc.) |

### 4.4 Decision Logic Summary

```
IF http_detected AND has_web_server:
    → Recommend "nikto" (web vulnerability scan)
    
IF ssh_detected OR ftp_detected:
    → Recommend "hydra" (brute-force login)
    
IF has_auth_service AND open_ports <= 3:
    → Recommend "john" (offline password cracking)
    
IF has_web_server AND has_directory_listing:
    → Recommend "dirb" (directory brute-force)
```

---

## 5. Confidence Scoring

### 5.1 Confidence Calculation

```python
def calculate_confidence(self, features: dict) -> tuple[float, str]:
    """Calculate prediction confidence using predict_proba.
    
    Returns: (confidence_score, confidence_label)
    """
    probabilities = self.model.predict_proba([feature_vector])[0]
    confidence = max(probabilities)  # Highest class probability
    
    if confidence >= 0.75:
        label = "high"
    elif confidence >= 0.50:
        label = "medium"
    else:
        label = "low"
    
    return (confidence, label)
```

### 5.2 Confidence Thresholds

| Confidence Range | Label    | UI Behavior                                       |
|------------------|----------|---------------------------------------------------|
| 75% – 100%       | **High**   | ✅ "Recommended" badge, green highlight         |
| 50% – 74%        | **Medium** | ⚠️ "Suggested" badge, yellow highlight          |
| 0% – 49%         | **Low**    | ❓ "Low confidence" warning, gray display       |

### 5.3 Multi-Suggestion Support

When confidence is below 50%, the engine may return **top 2 suggestions**:

```python
def get_suggestions(self, features: dict) -> list[Prediction]:
    probabilities = self.model.predict_proba([feature_vector])[0]
    top_indices = probabilities.argsort()[-2:][::-1]
    
    suggestions = []
    for idx in top_indices:
        suggestions.append(Prediction(
            recommended_tool=self.label_map[idx],
            confidence=probabilities[idx],
            confidence_label=self._get_label(probabilities[idx])
        ))
    return suggestions
```

---

## 6. Scoring Engine Performance Targets

| Metric                 | Target           | Measurement Method               |
|------------------------|------------------|----------------------------------|
| Prediction Accuracy    | > 70%            | Test set accuracy                |
| F1 Score               | > 0.65           | Weighted F1 across all classes   |
| Inference Time         | < 50ms           | Time from features to prediction |
| Model Load Time        | < 500ms          | Time to deserialize .pkl         |
| False Positive Rate    | < 15%            | Wrong recommendations            |

---

## 7. Model Versioning

| Version | Algorithm       | Features | Labels | Accuracy | Notes                          |
|---------|-----------------|----------|--------|----------|--------------------------------|
| v0.1    | Decision Tree   | 8        | 4      | 62%      | Initial prototype              |
| v0.2    | Random Forest   | 12       | 4      | 74%      | MVP release candidate          |
| v1.0    | Random Forest   | 15       | 4      | Target>70% | Production MVP              |
| v2.0    | Random Forest   | 20+      | 10-15  | Target>70% | Phase 2: expanded tool set  |
| v3.0    | *TBD*           | 30+      | 50+    | Target>70% | Phase 3: broad coverage     |

---

## 8. Edge Cases & Fallback Behavior

| Scenario                           | Behavior                                  |
|------------------------------------|-------------------------------------------|
| Model file not found               | Skip ML, show "ML unavailable" message    |
| All features are zero              | Skip ML, show "Insufficient data" message |
| Confidence below 30%               | Show suggestion with strong warning       |
| Multiple tools equally likely      | Show top 2 with equal confidence          |
| Tool not available on system       | Flag suggestion as "Tool not installed"   |
| Feature extraction fails           | Skip ML, log error, show raw results only |
