# Kalinova

Kalinova is a PyQt6 desktop control center for ethical security testing workflows on Kali Linux.

This README is optimized for both humans and AI coding assistants (Claude, Copilot, Codex) so work can continue across sessions with minimal conflicts.

## Project Goal

Convert security tools from raw CLI usage into a guided workflow with:
- Tool-specific GUI forms
- Command execution + live output streaming
- Risk scoring based on detected signals
- Suggested next actions
- Session logging and report generation

## Current Code Reality

As of code inspection on 2026-05-18:
- App entry point is `main.py` (creates `MainWindow`)
- UI modules exist for Dashboard, Recon, Web, Auth, Network, Reports, Settings
- Tool command builders exist for 12 tools: `nmap`, `whois`, `theHarvester`, `nikto`, `sqlmap`, `gobuster`, `hydra`, `john`, `nc`, `wireshark`, `wifite`, `autopsy`
- Command execution runs in `core.executor.CommandThread`
- Risk scoring is in `core.risk_engine.RiskEngine`
- Suggestions are in `core.suggestion_engine.SuggestionEngine`
- Shared global state is in `core.app_state.app_state`
- Logging writes into `logs/`
- PDF report generation exists in `core.report_generator`
- `parser/nmap_parser.py`, `parser/web_parser.py`, and `config.py` are currently placeholders/empty

## Repository Map

```text
kalinova/
  main.py
  config.py
  README.md
  core/
    app_state.py
    executor.py
    log_manager.py
    port_parser.py
    report_generator.py
    risk_engine.py
    suggestion_engine.py
  parser/
    nmap_parser.py
    web_parser.py
  tools/
    nmap_gui.py
    nikto_gui.py
    whois_gui.py
  ui/
    main_window.py
    workspace.py
    sidebar.py
    topbar.py
    console.py
    dashboard_page.py
    recon_page.py
    web_page.py
    auth_page.py
    network_page.py
    reports_page.py
    settings_page.py
    tool_template.py
    tool_icon_button.py
```

## Runtime Flow

1. `main.py` starts `QApplication` and `MainWindow`.
2. Page widgets emit `run_command(str)` from UI modules.
3. `core.executor.CommandThread` runs command via subprocess, streams stdout, logs output.
4. `core.port_parser` + event detection update `app_state`.
5. `core.risk_engine` recalculates risk.
6. `core.suggestion_engine` updates next-step guidance.
7. Console and UI reflect new state.

## Local Run

1. Create and activate a Python virtual environment.
2. Install dependencies: `pip install PyQt6 reportlab`
3. Run:

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

- `ui/*`: page layout, inputs, and command builder wiring
- `core/executor.py`: command execution pipeline and event detection
- `core/app_state.py`: shared state contract
- `core/risk_engine.py`: scoring logic only
- `core/suggestion_engine.py`: recommendation logic only
- `core/log_manager.py` and `core/report_generator.py`: output persistence/reporting

If a task touches multiple boundaries, implement in small steps and verify each step.

### 4) Verification Before Handoff

- Run targeted checks for edited files.
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

- Phase 1: foundation UI + execution core (implemented)
- Phase 2: tool module integration and polish (in progress)
- Phase 3: intelligence scoring/suggestions refinement (in progress)
- Phase 4: richer logging/reporting outputs (partially implemented)
- Phase 5: custom Kali ISO packaging (planned)

## Ethical Use

This project is for legal, authorized, and educational security testing only.

Do not run scans against systems you do not own or have explicit permission to test.
