# Kalinova — System Architecture Document

**Version:** 1.0 | **Date:** 2026-03-03

---

## 1. Architectural Style — Layered Modular Architecture

```
┌──────────────────────────────────────────┐
│          PRESENTATION LAYER              │
│     (PyQt6 GUI — Dashboard + Tools)      │
├──────────────────────────────────────────┤
│          EXECUTION LAYER                 │
│     (QProcess Wrapper + CommandBuilder)   │
├──────────────────────────────────────────┤
│          PARSING LAYER                   │
│     (Tool-Specific Output Parsers)        │
├──────────────────────────────────────────┤
│          TOOL-TYPE HANDLER LAYER         │
│     (Output Behavior Routing)             │
├──────────────────────────────────────────┤
│          INTELLIGENCE LAYER              │
│     (ML Feature Extraction + Prediction)  │
├──────────────────────────────────────────┤
│          OUTPUT LAYER                    │
│     (Suggestions + Reports + Display)     │
└──────────────────────────────────────────┘
```

---

## 2. Layer Specifications

### 2.1 Presentation Layer (PyQt6)
- `MainDashboard` — Central hub with tool cards
- `ToolWindow` — Per-tool GUI with input form + results
- `SuggestionPanel` — ML recommendations (assessment only)
- `ResultsPanel` — Structured output display
- `DisclaimerDialog` — First-launch legal consent

### 2.2 Execution Layer (QProcess)
- `ProcessRunner` — Wraps QProcess, manages start/stop/cancel
- `CommandBuilder` — Constructs CLI strings from GUI inputs
- States: `IDLE → STARTING → RUNNING → COMPLETED / CANCELLED / ERROR`

### 2.3 Parsing Layer
Each tool has a dedicated parser. The system is designed so that **adding a new parser is a plug-in operation** — create a class extending `BaseParser`, register it, and it works.

MVP Parsers:
- `NmapParser` → `{"hosts": [...], "open_ports": [...]}`
- `NiktoParser` → `{"vulnerabilities": [...], "server": "..."}`
- `JohnParser` → `{"cracked": [...], "status": "..."}`
- `HydraParser` → `{"found_credentials": [...]}`

Future parsers (Dirb, Gobuster, sqlmap, Aircrack-ng, enum4linux, etc.) follow the same pattern.

### 2.4 Tool-Type Handler
Routes parsed data based on declared type:
- `assessment` → full report + risk tags + ML suggestion
- `action` → structured summary only
- `utility` → basic formatted text

### 2.5 Intelligence Layer (scikit-learn)
- `FeatureExtractor` — Converts parsed dict to numeric vector
- `ModelLoader` — Loads `.pkl` via joblib
- `Predictor` — Returns recommended tool + confidence score
- Algorithm: Decision Tree / Random Forest
- Only triggers for assessment-type tools

### 2.6 Output Layer
- `SuggestionRenderer` — Formats ML prediction
- `ReportGenerator` — HTML report from template
- `RiskClassifier` — Tags findings (Critical/High/Medium/Low/Info)

---

## 3. Technology Stack

| Layer              | Technology        | Version  |
|--------------------|-------------------|----------|
| Language           | Python            | 3.10+    |
| GUI                | PyQt6             | 6.x      |
| Process Execution  | QProcess (Qt)     | —        |
| Machine Learning   | scikit-learn      | 1.x      |
| Serialization      | joblib            | 1.x      |
| Packaging          | dpkg-deb          | —        |
| OS Target          | Kali Linux        | 2023.x+  |

---

## 4. Deployment Architecture

Installed to `/opt/kalinova/` via `.deb` package. Desktop entry added to `/usr/share/applications/`. Zero modification to Kali system binaries. All processing is local — no network services required.

---

## 5. Security Architecture

- No forced privilege escalation
- No system file modification
- No external data transmission
- ML model is read-only and bundled
- Legal disclaimer on first launch

---

## 6. Extensibility — Adding a New Tool

1. Create GUI → `gui/tools/new_tool_window.py` (or use auto-generated form from YAML config)
2. Create Parser → `parsers/new_tool_parser.py`
3. Declare type → Register in `tool_registry.py` (or via YAML/JSON plugin file)
4. Add to Dashboard → Auto-discovered from registry

No core modification required — pure plug-in architecture. **This pattern enables scaling to 600+ tools** by allowing tool additions through configuration files alone (post-plugin system implementation).

---

## 7. Error Handling

| Error Type         | Handling                                |
|--------------------|-----------------------------------------|
| Tool not found     | "Tool not installed" message            |
| Permission denied  | "Run with appropriate permissions"      |
| Timeout            | Cancel process, show timeout message    |
| Parsing failure    | Show raw output + "Unable to parse"     |
| ML model missing   | Skip suggestion, show "ML unavailable"  |
| Invalid input      | Inline validation before execution      |

---

## 8. Performance Targets

| Aspect             | Target        | Approach                    |
|--------------------|---------------|-----------------------------|
| GUI Responsiveness | <100ms        | Async QProcess execution    |
| Model Load Time    | <500ms        | Cache model at startup      |
| Parsing Time       | <100ms        | Efficient regex parsing     |
| Memory Usage       | <200MB        | No large in-memory datasets |
| Startup Time       | <3 seconds    | Lazy-load tool windows      |
