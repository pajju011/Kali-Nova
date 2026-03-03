# Kalinova — Monorepo Structure

**Version:** 1.0 | **Date:** 2026-03-03

---

## 1. Overview

Kalinova uses a **monorepo** structure organized by architectural layer. All source code, models, assets, tests, documentation, and packaging scripts reside in a single repository. The structure is designed to **scale from 4 MVP tools to all 600+ Kali Linux tools** through a plugin-based tool registration system. New tools can be added by creating plugin definition files without modifying core code.

---

## 2. Repository Structure

```
kalinova/
│
├── README.md                          # Project overview & quickstart
├── LICENSE                            # License file
├── CHANGELOG.md                       # Version history
├── Makefile                           # Build, test, package commands
├── requirements.txt                   # Python dependencies
├── setup.py                           # Python package setup
├── .gitignore                         # Git ignore rules
├── .github/                           # GitHub CI/CD workflows
│   └── workflows/
│       ├── ci.yml                     # Lint, test, build pipeline
│       └── release.yml                # .deb package build & release
│
├── src/                               # Main source code
│   └── kalinova/
│       ├── __init__.py
│       ├── main.py                    # Application entry point
│       ├── app.py                     # QApplication setup & initialization
│       │
│       ├── gui/                       # Presentation Layer
│       │   ├── __init__.py
│       │   ├── dashboard.py           # Central dashboard window
│       │   ├── disclaimer_dialog.py   # First-launch legal disclaimer
│       │   ├── base_tool_window.py    # Abstract base for tool GUIs
│       │   ├── results_panel.py       # Reusable results display widget
│       │   ├── suggestion_panel.py    # ML suggestion display widget
│       │   ├── report_viewer.py       # HTML report preview dialog
│       │   ├── tools/                 # Tool-specific GUI windows
│       │   │   ├── __init__.py
│       │   │   ├── nmap_window.py
│       │   │   ├── nikto_window.py
│       │   │   ├── john_window.py
│       │   │   └── hydra_window.py
│       │   ├── widgets/               # Reusable custom widgets
│       │   │   ├── __init__.py
│       │   │   ├── tool_card.py       # Dashboard tool card widget
│       │   │   ├── risk_badge.py      # Severity badge widget
│       │   │   ├── loading_spinner.py # Progress indicator
│       │   │   └── input_field.py     # Validated input field widget
│       │   └── styles/                # Qt stylesheets
│       │       ├── dark_theme.qss
│       │       └── light_theme.qss
│       │
│       ├── core/                      # Execution Layer
│       │   ├── __init__.py
│       │   ├── process_runner.py      # QProcess wrapper
│       │   ├── command_builder.py     # CLI command constructor
│       │   ├── tool_registry.py       # Tool type registry & config
│       │   └── exceptions.py          # Custom exception hierarchy
│       │
│       ├── parsers/                   # Parsing Layer (extensible for 600+ tools)
│       │   ├── __init__.py
│       │   ├── base_parser.py         # Abstract parser interface
│       │   ├── nmap_parser.py         # Nmap output parser
│       │   ├── nikto_parser.py        # Nikto output parser
│       │   ├── john_parser.py         # John output parser
│       │   ├── hydra_parser.py        # Hydra output parser
│       │   └── ...                    # Future parsers added here (dirb, sqlmap, etc.)
│       │
│       ├── handlers/                  # Tool-Type Handler Layer
│       │   ├── __init__.py
│       │   ├── type_handler.py        # Output routing by tool type
│       │   └── risk_classifier.py     # Finding severity classifier
│       │
│       ├── ml/                        # Intelligence Layer
│       │   ├── __init__.py
│       │   ├── feature_extractor.py   # Parsed data → feature vector
│       │   ├── predictor.py           # Model loading & prediction
│       │   └── training/              # Model training scripts (dev)
│       │       ├── train_model.py
│       │       ├── generate_dataset.py
│       │       └── evaluate_model.py
│       │
│       ├── reports/                   # Output Layer — Reporting
│       │   ├── __init__.py
│       │   ├── report_generator.py    # HTML report generation
│       │   └── templates/
│       │       └── report_template.html
│       │
│       ├── db/                        # Data Layer
│       │   ├── __init__.py
│       │   ├── database.py            # SQLite connection manager
│       │   ├── models.py              # ORM / dataclass models
│       │   └── migrations/            # Schema migration scripts
│       │       └── 001_initial.sql
│       │
│       ├── config/                    # Configuration
│       │   ├── __init__.py
│       │   ├── settings.py            # App settings & defaults
│       │   └── defaults/
│       │       ├── app.json           # Default app config
│       │       └── preferences.json   # Default user preferences
│       │
│       ├── plugins/                   # Plugin System (for scalable tool addition)
│       │   ├── __init__.py
│       │   ├── plugin_loader.py       # Discovers & loads tool plugins
│       │   ├── plugin_validator.py    # Validates plugin definitions
│       │   └── tool_definitions/      # YAML/JSON tool definition files
│       │       ├── nmap.yaml          # Nmap tool definition
│       │       ├── nikto.yaml         # Nikto tool definition
│       │       ├── john.yaml          # John tool definition
│       │       ├── hydra.yaml         # Hydra tool definition
│       │       └── ...               # Add new tools here as YAML files
│       │
│       └── utils/                     # Shared utilities
│           ├── __init__.py
│           ├── logger.py              # Logging configuration
│           ├── validators.py          # Input validation helpers
│           └── file_utils.py          # File I/O helpers
│
├── models/                            # Pre-trained ML models
│   └── next_tool_model.pkl
│
├── assets/                            # Static assets
│   ├── icons/
│   │   ├── kalinova_logo.png
│   │   ├── nmap_icon.png
│   │   ├── nikto_icon.png
│   │   ├── john_icon.png
│   │   └── hydra_icon.png
│   └── images/
│       └── splash_screen.png
│
├── tests/                             # Test suite
│   ├── __init__.py
│   ├── conftest.py                    # Shared test fixtures
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_nmap_parser.py
│   │   ├── test_nikto_parser.py
│   │   ├── test_john_parser.py
│   │   ├── test_hydra_parser.py
│   │   ├── test_command_builder.py
│   │   ├── test_feature_extractor.py
│   │   ├── test_predictor.py
│   │   ├── test_risk_classifier.py
│   │   └── test_report_generator.py
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_execution_pipeline.py
│   │   ├── test_parsing_pipeline.py
│   │   └── test_ml_pipeline.py
│   └── e2e/
│       ├── __init__.py
│       └── test_full_scan_flow.py
│
├── docs/                              # Documentation
│   ├── product_requirement.md
│   ├── user_stories.md
│   ├── system_architecture.md
│   ├── database_schema.md
│   ├── api_contracts.md
│   ├── development_phases.md
│   └── contributing.md
│
└── packaging/                         # Debian packaging
    ├── build_deb.sh                   # .deb build script
    ├── DEBIAN/
    │   ├── control                    # Package metadata
    │   ├── postinst                   # Post-install script
    │   └── prerm                      # Pre-removal script
    └── usr/
        └── share/
            └── applications/
                └── kalinova.desktop   # Desktop entry file
```

---

## 3. Layer-to-Directory Mapping

| Architecture Layer     | Directory                   | Key Files                         |
|------------------------|-----------------------------|-----------------------------------|
| Presentation           | `src/kalinova/gui/`         | dashboard.py, tools/*.py          |
| Execution              | `src/kalinova/core/`        | process_runner.py, command_builder|
| Parsing                | `src/kalinova/parsers/`     | *_parser.py                       |
| Tool-Type Handler      | `src/kalinova/handlers/`    | type_handler.py, risk_classifier  |
| Intelligence (ML)      | `src/kalinova/ml/`          | predictor.py, feature_extractor   |
| Output (Reports)       | `src/kalinova/reports/`     | report_generator.py               |
| Data Persistence       | `src/kalinova/db/`          | database.py, models.py            |
| Configuration          | `src/kalinova/config/`      | settings.py                       |

---

## 4. Dependency Map

```
gui/ ──────▶ core/ ──────▶ (QProcess / CLI Tools)
  │            │
  │            ▼
  │         parsers/ ────▶ handlers/ ────▶ ml/
  │                                        │
  │                                        ▼
  └──────────────────────────────────▶ reports/
                                        │
                                        ▼
                                      db/
```

---

## 5. Key Configuration Files

| File                | Purpose                                   |
|---------------------|-------------------------------------------|
| `requirements.txt`  | Python package dependencies               |
| `Makefile`          | Build, test, lint, package commands       |
| `.github/workflows` | CI/CD pipeline definitions                |
| `setup.py`          | Package installation metadata             |
| `packaging/`        | .deb build scripts & metadata             |

---

## 6. Makefile Commands

```makefile
install:     pip install -r requirements.txt
run:         python -m kalinova.main
test:        pytest tests/ -v
test-unit:   pytest tests/unit/ -v
test-int:    pytest tests/integration/ -v
lint:        flake8 src/ && mypy src/
build-deb:   bash packaging/build_deb.sh
clean:       rm -rf build/ dist/ *.egg-info
```
