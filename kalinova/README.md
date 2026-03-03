# Kalinova — Intelligent GUI Security Suite for Kali Linux

> Terminal-free access to security tools with ML-powered next-step suggestions.

## Quick Start on Kali Linux

```bash
# 1. Clone or copy the project
cd kalinova/

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
cd src/
python -m kalinova.main
```

## Project Structure

```
kalinova/
├── src/kalinova/
│   ├── main.py                    # Entry point
│   ├── core/
│   │   ├── process_runner.py      # QProcess wrapper
│   │   ├── command_builder.py     # CLI command construction
│   │   ├── tool_registry.py       # Dynamic tool registry
│   │   ├── database.py            # SQLite storage
│   │   └── exceptions.py          # Error hierarchy
│   ├── parsers/
│   │   ├── base_parser.py         # Abstract parser
│   │   ├── nmap_parser.py         # Nmap output parser
│   │   ├── nikto_parser.py        # Nikto output parser
│   │   ├── john_parser.py         # John output parser
│   │   └── hydra_parser.py        # Hydra output parser
│   ├── handlers/
│   │   └── type_handler.py        # Assessment/Action/Utility routing
│   ├── ml/
│   │   ├── feature_extractor.py   # Feature extraction from parsed data
│   │   └── predictor.py           # ML prediction + rule-based fallback
│   ├── reporting/
│   │   └── report_generator.py    # HTML report generation
│   ├── gui/
│   │   ├── main_window.py         # Main application window
│   │   ├── dashboard.py           # Central tool hub
│   │   ├── disclaimer_dialog.py   # Legal consent dialog
│   │   ├── styles.py              # Global stylesheet
│   │   └── tools/
│   │       ├── base_tool_window.py # Abstract tool window
│   │       ├── nmap_window.py     # Nmap GUI
│   │       ├── nikto_window.py    # Nikto GUI
│   │       ├── john_window.py     # John GUI
│   │       └── hydra_window.py    # Hydra GUI
│   └── utils/
│       └── validators.py          # Input validation
├── packaging/                     # .deb package files
├── requirements.txt
├── pyproject.toml
├── Makefile
└── README.md
```

## Architecture

**Layered Modular Architecture:**

```
User → GUI (PyQt6) → CommandBuilder → ProcessRunner (QProcess)
           ↓                                    ↓
    Dashboard/Tools                 CLI Tool (nmap, nikto, etc.)
           ↓                                    ↓
    Results Display ← Parser ← Raw Output
           ↓
    TypeHandler → ML Predictor → Suggestion Panel
           ↓
    ReportGenerator → HTML Export
```

## Adding New Tools

1. Create parser in `src/kalinova/parsers/new_tool_parser.py`
2. Add command builder method in `core/command_builder.py`
3. Register tool in `core/tool_registry.py`
4. Create GUI window in `gui/tools/new_tool_window.py`
5. Register window in `gui/main_window.py`

## Build .deb Package

```bash
make build-deb
# Output: build/kalinova_1.0.0_amd64.deb

# Install on Kali
sudo dpkg -i build/kalinova_1.0.0_amd64.deb

# Uninstall
sudo dpkg -r kalinova
```

## Requirements

- **OS:** Kali Linux (Debian-based)
- **Python:** 3.10+
- **Tools:** Nmap, Nikto, John the Ripper, Hydra (pre-installed on Kali)
