# Kalinova — API Contracts Document

**Version:** 1.0 | **Date:** 2026-03-03

> **Scalability Note:** All interfaces are designed for **unlimited tool expansion**. New tools are added by implementing `BaseTool` and `BaseParser` — no core code changes required. The MVP ships with 4 tools; the architecture targets all 600+ Kali Linux tools.

---

## 1. Overview

Kalinova is a **desktop application** — it does not expose HTTP/REST APIs. This document defines the **internal API contracts** between Kalinova's modules: the interfaces, method signatures, data contracts, and event protocols that govern inter-layer communication.

---

## 2. Core Interfaces

### 2.1 BaseTool Interface

All tool implementations must conform to this contract.

```python
class BaseTool:
    """Base interface for all Kalinova tool wrappers."""

    name: str                    # e.g., "nmap"
    tool_type: str               # "assessment" | "action" | "utility"
    display_name: str            # e.g., "Nmap Scanner"
    description: str             # Beginner-friendly description
    ml_enabled: bool             # Whether ML suggestions apply

    def build_command(self, params: dict) -> list[str]:
        """Build CLI command from user input parameters.
        Args:   params — dict of user-provided inputs
        Returns: list of command parts, e.g. ["nmap", "-sV", "192.168.1.1"]
        Raises:  ValueError if required params missing
        """

    def validate_inputs(self, params: dict) -> tuple[bool, str]:
        """Validate user inputs before execution.
        Returns: (is_valid, error_message)
        """

    def get_parser(self) -> BaseParser:
        """Return the parser instance for this tool."""
```

### 2.2 BaseParser Interface

```python
class BaseParser:
    """Base interface for all output parsers."""

    def parse(self, raw_output: str) -> dict:
        """Parse raw CLI output into structured data.
        Args:   raw_output — stdout string from QProcess
        Returns: structured dictionary
        Raises:  ParsingError on failure
        """

    def get_findings(self, parsed_data: dict) -> list[Finding]:
        """Extract risk-classified findings from parsed data.
        Returns: list of Finding objects with severity levels
        """
```

### 2.3 ProcessRunner Interface

```python
class ProcessRunner(QObject):
    """Manages CLI tool execution via QProcess."""

    # Signals
    output_received = Signal(str)      # Emitted on stdout data
    error_received = Signal(str)       # Emitted on stderr data
    process_finished = Signal(int, str) # Emitted on completion (exit_code, output)
    process_error = Signal(str)        # Emitted on process error

    def start(self, command: list[str]) -> None:
        """Start tool execution. Args: command — list of command parts"""

    def cancel(self) -> None:
        """Cancel running process."""

    def is_running(self) -> bool:
        """Check if process is currently running."""

    def get_output(self) -> str:
        """Get accumulated stdout output."""

    def get_errors(self) -> str:
        """Get accumulated stderr output."""
```

### 2.4 MLPredictor Interface

```python
class MLPredictor:
    """ML prediction engine for next-tool suggestions."""

    def load_model(self, model_path: str) -> None:
        """Load trained model from .pkl file.
        Raises: FileNotFoundError, ModelLoadError
        """

    def extract_features(self, parsed_data: dict) -> dict:
        """Extract numeric features from parsed scan results.
        Returns: feature dictionary, e.g. {"open_ports": 3, "http_detected": 1}
        """

    def predict(self, features: dict) -> Prediction:
        """Run prediction and return result.
        Returns: Prediction(tool="nikto", confidence=0.85, label="high")
        """
```

### 2.5 ReportGenerator Interface

```python
class ReportGenerator:
    """Generates HTML reports from assessment results."""

    def generate(self, scan_data: ScanResult) -> str:
        """Generate HTML report string.
        Args:   scan_data — complete scan result with findings
        Returns: HTML string
        """

    def save(self, html: str, output_path: str) -> str:
        """Save report to disk.
        Returns: absolute file path of saved report
        """
```

---

## 3. Data Contracts (DTOs)

### 3.1 ScanParams

```python
@dataclass
class ScanParams:
    tool_name: str          # "nmap" | "nikto" | "john" | "hydra"
    target: str             # IP, URL, or file path
    options: dict           # Tool-specific options
    # Example: {"scan_type": "SYN", "port_range": "1-1000"}
```

### 3.2 ScanResult

```python
@dataclass
class ScanResult:
    tool_name: str
    tool_type: str          # "assessment" | "action" | "utility"
    target: str
    status: str             # "completed" | "cancelled" | "error"
    exit_code: int
    raw_output: str
    parsed_data: dict
    findings: list[Finding]
    started_at: datetime
    completed_at: datetime
    duration_ms: int
```

### 3.3 Finding

```python
@dataclass
class Finding:
    description: str
    severity: str           # "critical" | "high" | "medium" | "low" | "info"
    category: str           # "open_port" | "vulnerability" | "credential"
    details: dict
    explanation: str        # Beginner-friendly explanation
```

### 3.4 Prediction

```python
@dataclass
class Prediction:
    recommended_tool: str   # e.g., "nikto"
    confidence: float       # 0.0 - 1.0
    confidence_label: str   # "high" | "medium" | "low"
    reasoning: str          # Brief explanation
    features_used: dict     # Feature vector used for prediction
```

---

## 4. Event / Signal Contracts

### 4.1 GUI → Execution Layer

| Event              | Signal                  | Payload                     |
|--------------------|-------------------------|-----------------------------|
| User clicks "Scan" | `execute_requested`     | `ScanParams`                |
| User clicks Cancel | `cancel_requested`      | None                        |

### 4.2 Execution → Parsing Layer

| Event              | Signal                  | Payload                     |
|--------------------|-------------------------|-----------------------------|
| Process completes  | `process_finished`      | `(exit_code: int, output: str)` |
| Process errors     | `process_error`         | `error_message: str`        |

### 4.3 Parsing → Tool-Type Handler

| Event              | Signal                  | Payload                     |
|--------------------|-------------------------|-----------------------------|
| Parsing complete   | `parsing_complete`      | `ScanResult`                |
| Parsing failed     | `parsing_failed`        | `(raw_output: str, error: str)` |

### 4.4 Handler → Intelligence / Output

| Event              | Signal                  | Payload                     |
|--------------------|-------------------------|-----------------------------|
| Assessment ready   | `assessment_complete`   | `ScanResult`                |
| Prediction ready   | `prediction_ready`      | `Prediction`                |
| Report generated   | `report_generated`      | `file_path: str`            |

---

## 5. Tool-Specific Input Contracts

### 5.1 Nmap

```python
nmap_params = {
    "target": "192.168.1.1",           # Required
    "scan_type": "SYN",                # "SYN" | "TCP" | "UDP" | "PING"
    "port_range": "1-1000",            # Optional, default: all
    "service_detection": True,         # -sV flag
    "os_detection": False,             # -O flag
    "aggressive": False                # -A flag
}
```

### 5.2 Nikto

```python
nikto_params = {
    "target": "http://example.com",    # Required
    "port": 80,                        # Optional
    "ssl": False,                      # -ssl flag
    "tuning": "1234",                  # Optional tuning options
}
```

### 5.3 John

```python
john_params = {
    "hash_file": "/path/to/hashes.txt", # Required
    "wordlist": "/path/to/wordlist.txt", # Optional
    "format": "raw-md5",                 # Optional hash format
}
```

### 5.4 Hydra

```python
hydra_params = {
    "target": "192.168.1.1",           # Required
    "service": "ssh",                  # Required: "ssh"|"ftp"|"http-post"
    "username": "admin",               # Required (or username_file)
    "username_file": None,             # Alternative to username
    "password_file": "/path/to/pass.txt", # Required
    "port": 22,                        # Optional
    "threads": 16,                     # Optional
}
```

---

## 6. Error Contracts

```python
class KalinovaError(Exception): pass
class ToolNotFoundError(KalinovaError): pass
class ExecutionError(KalinovaError): pass
class ParsingError(KalinovaError): pass
class ModelLoadError(KalinovaError): pass
class ValidationError(KalinovaError): pass
```
