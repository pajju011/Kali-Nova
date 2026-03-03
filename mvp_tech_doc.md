# Kalinova MVP Technical Document

## 1. MVP Scope

The MVP includes:

Assessment Tools:
- Nmap GUI
- Nikto GUI

Action Tools:
- John GUI
- Hydra GUI

Features:
- Terminal-free execution
- Structured parsing
- Tool-type adaptive output
- ML next-step suggestion (assessment tools only)
- Basic HTML report export
- .deb installer

---

## 2. Technology Stack

Language:
- Python 3

GUI:
- PyQt6

Process Handling:
- QProcess

Machine Learning:
- scikit-learn
- joblib

Packaging:
- dpkg-deb

---

## 3. Functional Requirements

### Execution
- Run CLI tools in background
- No visible terminal
- Capture output
- Provide cancel functionality
- Display friendly error messages

### Output Adaptation
- assessment → full structured report
- action → structured summary
- utility → formatted output

### ML Suggestion
- Extract features from parsed results
- Load trained model
- Predict next recommended tool
- Display confidence percentage

---

## 4. Non-Functional Requirements

- Responsive UI
- Clean uninstall
- Stable execution
- Works on default Kali installation
- No system file modification

---

## 5. Out of Scope (MVP)

- 600+ tool support
- Custom Kali ISO
- Cloud-based ML
- Multi-user management