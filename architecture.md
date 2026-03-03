# Kalinova Architecture Document

## 1. Overview

Kalinova is an intelligent GUI-based security suite built as a modular layer over Kali Linux.  
It provides terminal-free access to selected security tools and uses Machine Learning to suggest next actions for beginner users.

Kalinova does NOT modify Kali core components. It operates as an independent application layer installed via .deb package.

---

## 2. Architectural Style

Layered Modular Architecture

User Interface Layer
↓
Execution Layer (QProcess Wrapper)
↓
Parser Layer
↓
Tool-Type Handler
↓
ML Intelligence Layer (Conditional)
↓
Suggestion & Reporting Layer

---

## 3. Core Layers

### 3.1 GUI Layer
- Built with PyQt6
- Tool-specific windows
- Central dashboard
- Suggestion panel
- Result display component

### 3.2 Execution Layer
- Uses QProcess
- Executes CLI tools silently
- Captures stdout and stderr
- Handles errors and exit codes
- Supports cancellation

### 3.3 Parser Layer
- Converts raw CLI output into structured dictionaries
- Tool-specific parser modules

### 3.4 Tool-Type Handler
Each tool declares:
- assessment
- action
- utility

System dynamically adapts output behavior based on type.

### 3.5 ML Layer
- Feature extractor
- Trained Decision Tree / Random Forest model
- Predicts next recommended tool
- Returns confidence score

Used primarily for assessment tools.

### 3.6 Reporting Layer
- Generates structured reports for assessment tools
- Provides summary output for action tools
- Basic formatted display for utility tools

---

## 4. Deployment Architecture

Installed via .deb package.

Installed to:
- /opt/kalinova

Desktop entries:
- /usr/share/applications/

No modification to Kali core or system binaries.

---

## 5. Design Principles

- Modular
- Tool-type adaptive output
- Separation of concerns
- Fully uninstallable
- Beginner-friendly
- Minimal system intrusion