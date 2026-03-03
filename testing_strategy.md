# Kalinova — Testing Strategy

**Version:** 1.0 | **Date:** 2026-03-03

---

## 1. Overview

This document defines the comprehensive testing strategy for Kalinova, covering all testing levels, tools, coverage targets, and quality gates. The strategy follows the **Testing Pyramid** approach with a strong foundation of unit tests, supplemented by integration and end-to-end tests.

> **Scalability Note:** The testing framework is designed to **automatically scale** as new tools are added. Parser tests are parameterized — adding a new tool's test fixtures automatically includes it in the suite. The MVP covers 4 tools, but the framework supports testing for all 600+ Kali Linux tools.

---

## 2. Testing Pyramid

```
            ┌─────────┐
            │  E2E    │   ~10% of tests
            │  Tests  │   Full scan workflows
            ├─────────┤
            │ Integr. │   ~25% of tests
            │  Tests  │   Cross-module pipelines
            ├─────────┤
            │  Unit   │   ~65% of tests
            │  Tests  │   Individual components
            └─────────┘
```

---

## 3. Testing Levels

### 3.1 Unit Tests

**Scope:** Individual functions, classes, and modules in isolation.  
**Tools:** pytest, pytest-mock  
**Location:** `tests/unit/`

| Module Under Test     | Test File                      | Key Test Cases                                |
|----------------------|--------------------------------|-----------------------------------------------|
| NmapParser           | `test_nmap_parser.py`          | Valid output, empty output, malformed output   |
| NiktoParser          | `test_nikto_parser.py`         | Standard vulns, no vulns, timeout output       |
| JohnParser           | `test_john_parser.py`          | Cracked hashes, no cracks, running status      |
| HydraParser          | `test_hydra_parser.py`         | Found credentials, no results, errors          |
| *Future Parsers*     | `test_<tool>_parser.py`        | *Same pattern — each new tool gets a test file* |
| CommandBuilder       | `test_command_builder.py`      | All tools, all option combinations             |
| FeatureExtractor     | `test_feature_extractor.py`    | Nmap features, Nikto features, edge cases      |
| Predictor            | `test_predictor.py`            | Model loading, prediction, confidence          |
| RiskClassifier       | `test_risk_classifier.py`      | All severity levels, edge cases                |
| ReportGenerator      | `test_report_generator.py`     | HTML output, template rendering                |
| ToolRegistry         | `test_tool_registry.py`        | Registration, lookup, type validation          |
| InputValidators      | `test_validators.py`           | IP, URL, file path, port validation            |
| **PluginLoader**     | `test_plugin_loader.py`        | YAML loading, validation, auto-discovery       |
| **PluginValidator**  | `test_plugin_validator.py`     | Schema validation, missing fields, bad configs |

**Example Unit Test:**

```python
class TestNmapParser:
    def test_parse_valid_output(self):
        """Parser should extract open ports from valid Nmap output."""
        raw = """Starting Nmap scan...
        22/tcp open  ssh     OpenSSH 8.9
        80/tcp open  http    Apache 2.4.54
        Nmap done: 1 IP address (1 host up)"""
        
        result = NmapParser().parse(raw)
        
        assert result["open_ports"] == 2
        assert len(result["hosts"][0]["ports"]) == 2
        assert result["hosts"][0]["ports"][0]["service"] == "ssh"

    def test_parse_empty_output(self):
        """Parser should handle empty output gracefully."""
        result = NmapParser().parse("")
        assert result["open_ports"] == 0
        assert result["hosts"] == []

    def test_parse_malformed_output(self):
        """Parser should raise ParsingError on malformed output."""
        with pytest.raises(ParsingError):
            NmapParser().parse("This is not Nmap output")
```

### 3.2 Integration Tests

**Scope:** Cross-module interactions and data flow between layers.  
**Tools:** pytest, pytest-qt  
**Location:** `tests/integration/`

| Pipeline Tested              | Test File                       | Description                                |
|-----------------------------|---------------------------------|--------------------------------------------|
| Execution → Parsing        | `test_execution_pipeline.py`   | ProcessRunner output flows to Parser       |
| Parsing → Type Handler     | `test_parsing_pipeline.py`     | Parsed data routes by tool type            |
| Parsing → ML Prediction    | `test_ml_pipeline.py`          | Parsed data → features → prediction        |
| Parsing → Report Gen       | `test_report_pipeline.py`      | Parsed data → HTML report generation       |
| GUI → Execution → Display  | `test_gui_pipeline.py`         | Full UI interaction flow (mocked tools)    |

**Example Integration Test:**

```python
class TestMLPipeline:
    def test_nmap_to_prediction(self):
        """Nmap parsed results should produce a valid ML prediction."""
        parsed_data = {
            "open_ports": 3,
            "hosts": [{"ports": [
                {"port": 22, "service": "ssh"},
                {"port": 80, "service": "http"},
                {"port": 443, "service": "https"}
            ]}]
        }
        
        features = FeatureExtractor().extract("nmap", parsed_data)
        prediction = Predictor("models/test_model.pkl").predict(features)
        
        assert prediction.recommended_tool in ["nikto", "hydra", "john"]
        assert 0.0 <= prediction.confidence <= 1.0
        assert prediction.confidence_label in ["high", "medium", "low"]
```

### 3.3 End-to-End (E2E) Tests

**Scope:** Complete user workflows from GUI input to result display.  
**Tools:** pytest-qt, QTest  
**Location:** `tests/e2e/`

| Workflow                    | Test File                   | Description                                  |
|----------------------------|-----------------------------|----------------------------------------------|
| Full Nmap Scan             | `test_full_scan_flow.py`   | Dashboard → Nmap → Input → Scan → Results   |
| Assessment + Suggestion    | `test_assessment_flow.py`  | Nmap scan → ML suggestion → confidence       |
| Report Generation          | `test_report_flow.py`      | Nmap scan → Export → HTML file saved          |
| Cancel Scan                | `test_cancel_flow.py`      | Start scan → Cancel → UI returns to ready    |
| Error Handling             | `test_error_flow.py`       | Invalid input → Error message displayed       |

**Note:** E2E tests use **mocked CLI tools** to avoid requiring Nmap/Nikto/John/Hydra installation in CI.

---

## 4. Test Data Strategy

### 4.1 Test Fixtures

| Fixture                   | Location                        | Description                          |
|---------------------------|---------------------------------|--------------------------------------|
| Nmap sample outputs       | `tests/fixtures/nmap/`          | Valid, empty, error CLI outputs      |
| Nikto sample outputs      | `tests/fixtures/nikto/`         | Various vulnerability reports        |
| John sample outputs       | `tests/fixtures/john/`          | Cracked / no-crack outputs           |
| Hydra sample outputs      | `tests/fixtures/hydra/`         | Found / not-found credentials        |
| ML test model             | `tests/fixtures/models/`        | Small test model for CI              |
| Expected parsed results   | `tests/fixtures/expected/`      | Gold-standard parsed dictionaries    |

### 4.2 Fixture Example

```
tests/fixtures/nmap/
├── basic_scan.txt          # Standard scan output
├── detailed_scan.txt       # -sV -A scan output
├── no_hosts_up.txt         # No hosts found
├── permission_denied.txt   # Root required error
└── timeout.txt             # Scan timeout output
```

---

## 5. Coverage Targets

| Scope              | Target Coverage | Measurement                   |
|--------------------|-----------------|-------------------------------|
| Overall            | > 80%           | `pytest --cov`                |
| Parsers            | > 90%           | Critical data transformation  |
| ML Engine          | > 85%           | Prediction accuracy + code    |
| Core (Process)     | > 80%           | Execution paths               |
| GUI                | > 60%           | Widget logic (not rendering)  |
| Handlers           | > 85%           | Routing logic                 |
| Report Generator   | > 80%           | Template rendering            |

---

## 6. Quality Gates

### 6.1 Pull Request Quality Gate

| Check               | Threshold          | Blocking? |
|---------------------|--------------------|-----------|
| Unit tests pass     | 100% pass          | ✅ Yes    |
| Integration tests   | 100% pass          | ✅ Yes    |
| Code coverage       | > 80%              | ✅ Yes    |
| Linting (flake8)    | 0 errors           | ✅ Yes    |
| Type checking (mypy)| 0 errors           | ✅ Yes    |
| Code formatting     | Black compliant    | ✅ Yes    |

### 6.2 Release Quality Gate

| Check                | Threshold          | Blocking? |
|---------------------|--------------------|-----------|
| All PR gates pass   | 100%               | ✅ Yes    |
| E2E tests pass      | 100%               | ✅ Yes    |
| ML accuracy         | > 70%              | ✅ Yes    |
| .deb install test   | Pass               | ✅ Yes    |
| .deb uninstall test | Pass               | ✅ Yes    |
| No critical bugs    | 0                  | ✅ Yes    |
| No high bugs        | 0                  | ✅ Yes    |

---

## 7. Specialized Testing

### 7.1 Parser Robustness Testing

Since parsers handle raw CLI output that may vary across tool versions:

| Scenario                          | Test Approach                          |
|-----------------------------------|----------------------------------------|
| Standard output                   | Parse and verify all fields            |
| Empty output                      | Graceful handling, default values      |
| Partial output (cancelled scan)   | Parse available data, flag incomplete  |
| Malformed output                  | Raise ParsingError                     |
| Different tool versions           | Version-specific fixture files         |
| Unicode / special characters      | Encoding handling tests                |

### 7.2 ML Model Testing

| Test Type                    | Description                                  |
|------------------------------|----------------------------------------------|
| Accuracy test                | Run model on held-out test set (>70%)        |
| Feature extraction test      | Verify correct features from sample data     |
| Prediction consistency       | Same input → same output (deterministic)     |
| Confidence calibration       | High confidence → correct more often         |
| Edge case: all zeros         | Handle gracefully (no crash)                 |
| Edge case: missing features  | Handle gracefully with defaults              |
| Model file corruption        | Raise ModelLoadError                         |
| Model file missing           | Raise FileNotFoundError, skip ML             |

### 7.3 GUI Testing

| Test Type                    | Tool          | Description                          |
|------------------------------|---------------|--------------------------------------|
| Widget rendering             | pytest-qt     | Widgets display correctly            |
| Button click handlers        | pytest-qt     | Correct signals emitted              |
| Input validation feedback    | pytest-qt     | Error messages shown for bad input   |
| Loading state                | pytest-qt     | Spinner shows during execution       |
| Results display              | pytest-qt     | Parsed data renders in table         |

### 7.4 Installation Testing

| Test                          | Expected Result                        |
|-------------------------------|----------------------------------------|
| Fresh install on Kali         | Files in /opt/kalinova, desktop entry  |
| Install with missing deps     | dpkg reports missing dependencies      |
| Uninstall                     | All files removed cleanly              |
| Reinstall over existing       | Clean upgrade, no conflicts            |
| Launch after install          | Application starts and shows dashboard |

---

## 8. Test Execution Commands

```bash
# Run all tests
pytest tests/ -v

# Run only unit tests
pytest tests/unit/ -v

# Run only integration tests
pytest tests/integration/ -v

# Run only E2E tests
pytest tests/e2e/ -v

# Run with coverage report
pytest tests/ -v --cov=src/kalinova --cov-report=html

# Run specific test file
pytest tests/unit/test_nmap_parser.py -v

# Run tests matching a pattern
pytest tests/ -v -k "nmap"

# Run with fail-fast (stop on first failure)
pytest tests/ -v -x
```

---

## 9. Bug Severity Classification

| Severity   | Definition                                         | SLA         |
|------------|-----------------------------------------------------|-------------|
| Critical   | Application crash, data loss, security vulnerability | Fix in 24h  |
| High       | Feature completely broken, no workaround            | Fix in 48h  |
| Medium     | Feature partially broken, workaround exists         | Fix in 1wk  |
| Low        | Cosmetic issue, minor inconvenience                 | Fix in 2wk  |

---

## 10. Scaling Testing to 600+ Tools

As the tool library expands, the testing strategy scales via:

| Strategy                       | Approach                                                       |
|--------------------------------|----------------------------------------------------------------|
| Parameterized parser tests     | Each parser follows `BaseParser` — shared test harness          |
| Fixture-based test data        | Add `tests/fixtures/<tool>/` for each new tool                  |
| Plugin validation tests        | Auto-validate all YAML tool definitions on CI                   |
| Contract testing               | Verify all parsers return data matching `ScanResult` schema     |
| Regression test automation     | Adding a tool must not break existing tools                     |
| Community contribution tests   | PR template requires test fixtures for new tool submissions     |
