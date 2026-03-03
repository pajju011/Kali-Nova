# Kalinova — Environment & DevOps

**Version:** 1.0 | **Date:** 2026-03-03

---

## 1. Development Environment

### 1.1 Prerequisites

| Tool              | Version   | Purpose                          |
|-------------------|-----------|----------------------------------|
| Kali Linux        | 2023.x+   | Target OS                        |
| Python            | 3.10+     | Application language             |
| pip               | 22.0+     | Python package manager           |
| PyQt6             | 6.x       | GUI framework                    |
| Git               | 2.34+     | Version control                  |
| dpkg-deb          | System    | .deb package building            |
| virtualenv/venv   | System    | Python virtual environment       |

### 1.2 Local Setup

```bash
# 1. Clone repository
git clone https://github.com/kalinova/kalinova.git
cd kalinova

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
python -m kalinova.main

# 5. Run tests
pytest tests/ -v

# 6. Lint code
flake8 src/ && mypy src/

# 7. Add a new tool (plugin-based)
# Create YAML definition in src/kalinova/plugins/tool_definitions/
# Create parser in src/kalinova/parsers/
# Tool auto-discovered on next launch
```

### 1.3 Dependencies (`requirements.txt`)

```
PyQt6>=6.5.0
scikit-learn>=1.3.0
joblib>=1.3.0
jinja2>=3.1.0
pytest>=7.4.0
pytest-qt>=4.2.0
flake8>=6.1.0
mypy>=1.5.0
black>=23.7.0
isort>=5.12.0
coverage>=7.3.0
```

### 1.4 Development Tools

| Tool    | Purpose                     | Config File            |
|---------|-----------------------------|------------------------|
| Black   | Code formatting             | `pyproject.toml`       |
| isort   | Import sorting              | `pyproject.toml`       |
| Flake8  | Linting                     | `.flake8`              |
| MyPy    | Type checking               | `mypy.ini`             |
| pytest  | Testing                     | `pytest.ini`           |
| pre-commit | Pre-commit hooks         | `.pre-commit-config.yaml` |

---

## 2. Version Control Strategy

### 2.1 Branching Model — Git Flow (Simplified)

```
main ─────────────────────────────────────── (production-ready)
  │
  ├── develop ────────────────────────────── (integration branch)
  │     │
  │     ├── feature/nmap-gui ──────────────
  │     ├── feature/nikto-parser ──────────
  │     ├── feature/ml-engine ─────────────
  │     └── fix/parser-crash ──────────────
  │
  └── release/v1.0 ──────────────────────── (release candidate)
```

### 2.2 Branch Naming Convention

| Pattern                | Example                      | Usage                |
|------------------------|------------------------------|----------------------|
| `feature/<name>`       | `feature/nmap-gui`           | New feature          |
| `fix/<name>`           | `fix/parser-null-output`     | Bug fix              |
| `refactor/<name>`      | `refactor/process-runner`    | Code refactoring     |
| `docs/<name>`          | `docs/api-contracts`         | Documentation        |
| `release/v<version>`   | `release/v1.0`               | Release preparation  |

### 2.3 Commit Message Convention

```
<type>(<scope>): <description>

feat(gui): add Nmap tool window with input form
fix(parser): handle empty Nmap output gracefully
test(ml): add unit tests for feature extractor
docs(api): update parser interface contract
chore(ci): add flake8 to CI pipeline
```

---

## 3. CI/CD Pipeline

### 3.1 Pipeline Architecture

```
Push/PR to develop
        │
        ▼
┌───────────────┐
│    Lint        │  flake8, mypy, black --check
└───────┬───────┘
        │ pass
        ▼
┌───────────────┐
│  Unit Tests   │  pytest tests/unit/ -v
└───────┬───────┘
        │ pass
        ▼
┌───────────────┐
│ Integration   │  pytest tests/integration/ -v
│   Tests       │
└───────┬───────┘
        │ pass
        ▼
┌───────────────┐
│  Coverage     │  coverage report (>80%)
│   Report      │
└───────────────┘

Merge to main
        │
        ▼
┌───────────────┐
│  Build .deb   │  bash packaging/build_deb.sh
└───────┬───────┘
        │
        ▼
┌───────────────┐
│  Install Test │  dpkg -i + smoke test on Kali
└───────┬───────┘
        │
        ▼
┌───────────────┐
│  Release      │  GitHub Release + artifact upload
└───────────────┘
```

### 3.2 GitHub Actions — CI Workflow (`.github/workflows/ci.yml`)

```yaml
name: CI Pipeline
on:
  push:
    branches: [develop, main]
  pull_request:
    branches: [develop]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.10' }
      - run: pip install flake8 mypy black isort
      - run: black --check src/
      - run: isort --check-only src/
      - run: flake8 src/
      - run: mypy src/

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.10' }
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v --cov=src/ --cov-report=xml
      - uses: codecov/codecov-action@v3

  build:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - run: bash packaging/build_deb.sh
      - uses: actions/upload-artifact@v4
        with:
          name: kalinova-deb
          path: build/kalinova_*.deb
```

---

## 4. Environments

| Environment   | Purpose                  | Infrastructure          |
|---------------|--------------------------|-------------------------|
| **Local Dev** | Development & debugging  | Developer's Kali VM     |
| **CI**        | Automated testing        | GitHub Actions (Ubuntu) |
| **Staging**   | Pre-release validation   | Dedicated Kali VM       |
| **Production**| End-user installation    | User's Kali Linux       |

---

## 5. .deb Packaging

### 5.1 Package Metadata (`packaging/DEBIAN/control`)

```
Package: kalinova
Version: 1.0.0
Section: utils
Priority: optional
Architecture: all
Depends: python3 (>= 3.10), python3-pyqt6, nmap, nikto, john, hydra
Maintainer: Kalinova Team <team@kalinova.dev>
Description: Intelligent GUI security suite for Kali Linux
 Kalinova provides terminal-free access to selected security tools
 with ML-powered next-step suggestions for beginners.
```

### 5.2 Build Script (`packaging/build_deb.sh`)

```bash
#!/bin/bash
set -e
VERSION="1.0.0"
BUILD_DIR="build/kalinova_${VERSION}"
mkdir -p "${BUILD_DIR}/opt/kalinova"
mkdir -p "${BUILD_DIR}/usr/share/applications"
cp -r src/kalinova/* "${BUILD_DIR}/opt/kalinova/"
cp -r models/ "${BUILD_DIR}/opt/kalinova/models/"
cp -r assets/ "${BUILD_DIR}/opt/kalinova/assets/"
cp -r packaging/DEBIAN "${BUILD_DIR}/"
cp packaging/usr/share/applications/kalinova.desktop \
   "${BUILD_DIR}/usr/share/applications/"
dpkg-deb --build "${BUILD_DIR}"
echo "Built: build/kalinova_${VERSION}.deb"
```

### 5.3 Post-Install Script (`packaging/DEBIAN/postinst`)

```bash
#!/bin/bash
chmod +x /opt/kalinova/main.py
echo "Kalinova installed successfully to /opt/kalinova"
```

### 5.4 Pre-Removal Script (`packaging/DEBIAN/prerm`)

```bash
#!/bin/bash
echo "Removing Kalinova..."
```

---

## 6. Monitoring & Logging

### 6.1 Application Logging

| Log Level | Usage                                          |
|-----------|-------------------------------------------------|
| DEBUG     | Detailed execution flow (dev only)              |
| INFO      | Tool execution start/end, ML predictions        |
| WARNING   | Low-confidence predictions, parsing fallbacks   |
| ERROR     | Tool failures, parsing errors, model load errors|
| CRITICAL  | Application crash, unrecoverable state          |

### 6.2 Log Configuration

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('~/.kalinova/kalinova.log'),
        logging.StreamHandler()
    ]
)
```

### 6.3 Log File Location

| File                          | Content                     |
|-------------------------------|-----------------------------|
| `~/.kalinova/kalinova.log`    | Application activity log    |
| `~/.kalinova/error.log`       | Error-level events only     |

---

## 7. Backup & Recovery

Since Kalinova is a desktop application with local storage:

| Data                | Backup Strategy                      |
|---------------------|--------------------------------------|
| Scan History (SQLite)| User-managed, exportable              |
| User Preferences     | JSON file, easily backed up           |
| Generated Reports    | Saved to user-specified directory     |
| ML Model             | Bundled with package, re-installable  |
