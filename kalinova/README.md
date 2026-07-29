# Kalinova

Kalinova is a PyQt6 desktop control center for ethical security testing workflows on Kali Linux.

This README is optimized for both humans and AI coding assistants (Claude, Copilot, Codex) so work can continue across sessions with minimal conflicts.

## Project Goal

Convert security tools from raw CLI usage into a guided workflow with:
- Tool-specific GUI forms & customizable execution parameters
- Command execution + live output streaming & event detection
- Risk scoring based on detected signals & severity metrics
- AI Copilot diagnostics with CVSS scoring and language-specific remediation code snippets (Python / Node.js)
- Interactive Network Topology visualization with animated target/port status
- SQLite persistent database storage (`kalinova.db`) for scan history
- PDF & HTML report generation and session logging

## Current Code Reality

As of code inspection on 2026-07-29:
- **App Entry Point**: `main.py` (instantiates `MainWindow` and initializes global configuration/database)
- **UI Modules**:
  - `ui/main_window.py`: Core application container with navigation, sidebar, topbar, console log streaming, and dynamic page switching.
  - `ui/dashboard_page.py`: Master intelligence center featuring high-risk alerts, AI remediation panel, threat gauges, and live Network Topology widget.
  - `ui/topology_widget.py`: Animated (20 FPS) radar sweep network visualizer showing real-time port states and active target nodes.
  - `ui/recon_page.py`: Reconnaissance tools (Nmap, Whois, theHarvester).
  - `ui/web_page.py`: Web security audit tools (Nikto, Sqlmap, Gobuster).
  - `ui/auth_page.py`: Authentication & cracking tools (Hydra, John the Ripper).
  - `ui/network_page.py`: Packet & network analysis tools (Netcat, Wireshark, Wifite, Autopsy).
  - `ui/reports_page.py`: Scan history database management, filterable scan tables, HTML/PDF export.
  - `ui/settings_page.py`: Application mode (Beginner / Professional) and execution settings.
- **Core Engine**:
  - `core/executor.py`: Asynchronous process runner (`CommandThread`), stdout streaming, and regex-based security event parser.
  - `core/app_state.py`: Centralized singleton state manager for threat level, risk score, discovered ports, events, and next-action workflows.
  - `core/ai_copilot.py`: Rule-based AI remediation engine delivering CVSS metrics, severity tags, and Python/Node.js code patches.
  - `core/database.py`: SQLite storage manager (`kalinova.db`) for scan logs, parameters, stdout output, and risk ratings.
  - `core/risk_engine.py`: Dynamic threat calculator based on open port profiles and detected vulnerabilities.
  - `core/suggestion_engine.py`: Context-aware next-step tool recommendation engine.
  - `core/report_generator.py`: PDF report builder using ReportLab.
  - `core/log_manager.py`: File-based session log writer.
- **Test Suite**:
  - `tests/test_executor_behavior.py`, `tests/test_main_window_behavior.py`, `tests/test_professional_suite.py`, `tests/test_tool_ui_behavior.py`.

## Repository Map

```text
kalinova/
├── main.py                     # Entry point for PyQt6 application
├── config.py                   # Configuration placeholders
├── kalinova.db                 # SQLite scan history database
├── README.md                   # Project documentation & guidelines
├── core/
│   ├── ai_copilot.py          # AI diagnostic & code remediation engine
│   ├── app_state.py           # Shared global runtime state manager
│   ├── database.py            # SQLite database persistence layer
│   ├── executor.py            # Process execution pipeline & output streaming
│   ├── log_manager.py         # Session log persistence
│   ├── port_parser.py         # Output parser for open port detection
│   ├── report_generator.py    # ReportLab PDF report compiler
│   ├── risk_engine.py         # Risk scoring calculation logic
│   └── suggestion_engine.py   # Automated next-action recommendation engine
├── parser/
│   ├── nmap_parser.py         # Specialized Nmap output parser
│   └── web_parser.py          # Specialized Web scanner parser
├── tools/
│   ├── nikto_gui.py           # Nikto GUI command builder
│   ├── nmap_gui.py            # Nmap GUI command builder
│   └── whois_gui.py           # Whois GUI command builder
├── ui/
│   ├── auth_page.py           # Authentication & Password tools page
│   ├── console.py             # Live console output stream widget
│   ├── dashboard_page.py      # Master intelligence dashboard & AI Copilot UI
│   ├── main_window.py         # Main application window & router
│   ├── network_page.py        # Network analysis & Wireless tools page
│   ├── recon_page.py          # Reconnaissance tools page
│   ├── reports_page.py        # SQLite history browser & report exporter
│   ├── settings_page.py       # Configuration & mode toggle settings
│   ├── sidebar.py             # Main navigation sidebar
│   ├── tool_icon_button.py    # Standardized tool action buttons
│   ├── tool_template.py       # Base GUI layout for security tool forms
│   ├── topbar.py              # Status bar & system info header
│   ├── topology_widget.py     # 20 FPS animated network topology canvas
│   ├── web_page.py            # Web vulnerability scanner page
│   └── workspace.py           # Active execution workspace container
└── tests/
    ├── test_executor_behavior.py      # Executor subprocess test cases
    ├── test_main_window_behavior.py   # UI navigation & main window tests
    ├── test_professional_suite.py     # End-to-end professional workflow suite
    └── test_tool_ui_behavior.py       # Tool form input & command generation tests
```

## Runtime Flow

1. `main.py` initializes SQLite schema (`kalinova.db`), starts `QApplication`, and opens `MainWindow`.
2. User selects tool parameters in UI modules and triggers execution.
3. `core.executor.CommandThread` spawns subprocess, streams stdout to console, and parses runtime output.
4. Discovered open ports and vulnerability signals are registered in `core.app_state`.
5. `core.risk_engine` and `core.ai_copilot` dynamically compute threat levels, CVSS scores, and code remediations.
6. `core.database.DatabaseManager` records scan parameters, stdout, and risk metadata to SQLite.
7. Dashboard updates live graphs, animated `NetworkTopologyWidget`, and recommended next actions.

## Local Run & Testing

1. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate   # On Windows
   source venv/bin/activate # On Linux/macOS
   ```
2. Install dependencies:
   ```bash
   pip install PyQt6 reportlab pytest
   ```
3. Run tests:
   ```bash
   pytest tests/
   ```
4. Launch application:
   ```bash
   python main.py
   ```

## AI Collaboration Protocol (Required)

Use this process for every AI session to avoid conflicts.

### 1) Pre-Edit Checklist

- Run `git status --short` and confirm what is already modified.
- Read this README and only the files needed for the requested change.
- Ignore generated folders: `venv/`, `__pycache__/`, runtime `logs/`, runtime `reports/`.

### 2) Scope Rules

- Change only the files directly needed for the task.
- Keep one logical task per commit or per handoff.
- Do not rename/move files unless explicitly requested.
- Do not combine behavior changes with broad formatting/style rewrites.

### 3) Ownership Boundaries

- `ui/*`: page layout, inputs, command builder wiring, topology visualizer
- `core/executor.py`: command execution pipeline and event detection
- `core/ai_copilot.py`: CVSS scoring, severity classification, and remediation snippets
- `core/database.py`: SQLite scan history schema and operations
- `core/app_state.py`: shared state contract
- `core/risk_engine.py`: scoring logic only
- `core/suggestion_engine.py`: recommendation logic only
- `core/log_manager.py` and `core/report_generator.py`: output persistence and PDF/HTML generation

If a task touches multiple boundaries, implement in small steps and verify each step.

### 4) Verification Before Handoff

- Run targeted checks for edited files or execute `pytest tests/`.
- If behavior changed, run the app and test the exact affected flow.
- Confirm no unintended file edits with `git status --short`.

### 5) Required Handoff Format

Every AI should end with this block so the next AI can continue safely:

```md
## AI Handoff
- Goal:
- Files changed:
- Behavior changed:
- Verification run:
- Open risks / assumptions:
- Next recommended step:
```

## Roadmap Snapshot

- Phase 1: Foundation UI + execution core (Completed)
- Phase 2: Tool module integration & UI polish (Completed)
- Phase 3: Intelligence scoring, suggestions, & AI Copilot diagnosis (Completed)
- Phase 4: Database persistence, network topology visualizer, & PDF/HTML reporting (Completed)
- Phase 5: Automated test suite coverage (Completed)
- Phase 6: Custom Kali ISO packaging & remote agent integration (Planned)

## Ethical Use

This project is for legal, authorized, and educational security testing only.

Do not run scans against systems you do not own or have explicit permission to test.
