# Kalinova — Product Requirements Document (Detailed)

**Version:** 1.0  
**Date:** 2026-03-03  
**Author:** Kalinova Product Team  
**Status:** Draft  

---

## 1. Product Vision

Kalinova is an intelligent, GUI-based security suite built as a modular application layer over Kali Linux. Its long-term goal is to provide GUI wrappers for **all 600+ Kali Linux tools**, eliminating the need for direct terminal interaction entirely. It leverages Machine Learning to suggest contextual next-step actions — making cybersecurity accessible to beginners. The MVP launches with an initial set of tools, but the architecture is designed from day one for **unlimited tool scalability**.

### 1.1 Mission Statement

> *"To democratize ethical hacking by providing a terminal-free, intelligent, and guided interface to Kali Linux security tools."*

### 1.2 Value Proposition

| Dimension           | Kali Linux (Current)                  | Kalinova (Proposed)                          |
|----------------------|---------------------------------------|----------------------------------------------|
| Interface            | CLI-only, 600+ tools                  | GUI wrappers with guided workflows           |
| Learning Curve       | Steep, assumes prior knowledge        | Beginner-friendly with explanations           |
| Output               | Raw terminal text                     | Structured, parsed, tool-type adaptive        |
| Guidance             | None                                  | ML-powered next-step suggestions              |
| Reporting            | Manual                                | Auto-generated HTML reports                   |

---

## 2. Target Users

### 2.1 Primary Users

| Persona                     | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| **Cybersecurity Students**   | University/college students learning ethical hacking and penetration testing |
| **Beginner Ethical Hackers** | Self-learners exploring Kali Linux tools without deep CLI experience        |

### 2.2 Secondary Users

| Persona                     | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| **Educators & Trainers**     | Instructors using Kalinova as a teaching aid for cybersecurity courses       |
| **CTF Participants**         | Capture-the-flag participants needing quick, visual tool execution           |

### 2.3 User Needs

1. Execute security tools without memorizing CLI syntax.
2. Understand tool output without deep networking knowledge.
3. Receive intelligent guidance on what to do next after a scan.
4. Generate professional reports for academic or professional use.
5. Install and uninstall cleanly without breaking the system.

---

## 3. Problem Statement

Kali Linux is the industry-standard platform for penetration testing, but it suffers from:

- **CLI Overload:** 600+ tools accessible only through terminal commands.
- **No Built-in Guidance:** Users must independently know which tool to use and in what order.
- **Raw Output:** Tool output is unstructured, verbose, and hard to interpret for beginners.
- **High Cognitive Load:** Requires memorization of flags, options, and tool chains.

Kalinova solves these problems by layering an intelligent GUI on top of Kali without modifying any system binaries.

---

## 4. Core Features

### 4.1 MVP Features (Phase 1)

| ID     | Feature                          | Priority  | Description                                                                 |
|--------|----------------------------------|-----------|-----------------------------------------------------------------------------|
| F-001  | Tool GUI Wrappers                | P0        | Clickable GUI windows — MVP: Nmap, Nikto, John, Hydra; expandable to 600+  |
| F-002  | Terminal-Free Execution          | P0        | All tools execute via QProcess with no visible terminal                      |
| F-003  | Structured Output Parsing        | P0        | Tool-specific parsers convert raw CLI output to structured dictionaries      |
| F-004  | Tool-Type Adaptive Output        | P0        | Output format adapts based on tool type (assessment/action/utility)          |
| F-005  | ML Next-Step Suggestion          | P0        | Decision Tree / Random Forest predicts next recommended tool                 |
| F-006  | Confidence Scoring               | P1        | ML predictions display confidence percentage                                |
| F-007  | HTML Report Export                | P1        | Assessment tools generate structured HTML reports                            |
| F-008  | Central Dashboard                | P0        | Main window showing all available tools and recent activity                  |
| F-009  | Beginner Explanation Panel       | P1        | Contextual explanations of what each tool does and its results mean          |
| F-010  | Risk Classification              | P1        | Findings are classified by risk severity (High / Medium / Low / Info)        |
| F-011  | .deb Package Installation        | P0        | Distributable as a Debian package installable via dpkg                       |

### 4.2 Post-MVP Features — Expanding the Tool Library

| ID     | Feature                          | Priority  | Description                                                                 |
|--------|----------------------------------|-----------|-----------------------------------------------------------------------------|
| F-012  | Tool Expansion Phase 2 (15-20)   | P1        | Add Dirb, Gobuster, enum4linux, sqlmap, Aircrack-ng, Burp CLI, etc.        |
| F-013  | Tool Expansion Phase 3 (50+)     | P2        | Cover all major Kali tool categories systematically                         |
| F-014  | Plugin System for Tool Addition  | P2        | YAML/JSON-based tool definition — add tools without code changes            |
| F-015  | Community Tool Contributions     | P2        | Allow community to submit tool wrappers via plugin format                   |
| F-016  | Full 600+ Tool Coverage          | P3        | Ultimate goal: GUI wrapper for every Kali Linux tool                        |
| F-017  | Scan History / Session Management| P2        | Persist and recall past scan results                                        |
| F-018  | Cloud-Based ML Model Updates     | P3        | Model retraining and updates via cloud                                      |
| F-019  | Multi-User Management            | P3        | User accounts and role-based access                                         |
| F-020  | Custom Kali ISO                  | P3        | Pre-bundled Kali ISO with Kalinova installed                                |

---

## 5. Functional Requirements

### 5.1 Execution Engine

| Req ID  | Requirement                                                              |
|---------|--------------------------------------------------------------------------|
| FR-001  | System SHALL execute CLI tools in the background using QProcess          |
| FR-002  | System SHALL capture both stdout and stderr from tool execution          |
| FR-003  | System SHALL provide cancel/abort functionality for running tools        |
| FR-004  | System SHALL display friendly error messages on tool failure             |
| FR-005  | System SHALL handle non-zero exit codes gracefully                       |

### 5.2 Output & Parsing

| Req ID  | Requirement                                                              |
|---------|--------------------------------------------------------------------------|
| FR-006  | System SHALL parse raw CLI output into structured Python dictionaries    |
| FR-007  | System SHALL adapt output format based on tool type declaration          |
| FR-008  | Assessment tools SHALL generate full structured reports                   |
| FR-009  | Action tools SHALL generate summary results                              |
| FR-010  | Utility tools SHALL display formatted output                             |

### 5.3 ML Suggestions

| Req ID  | Requirement                                                              |
|---------|--------------------------------------------------------------------------|
| FR-011  | System SHALL extract features from parsed assessment results             |
| FR-012  | System SHALL load a pre-trained scikit-learn model (.pkl) at runtime     |
| FR-013  | System SHALL predict the next recommended tool based on scan results     |
| FR-014  | System SHALL display the confidence percentage of each prediction        |
| FR-015  | ML suggestions SHALL only trigger for assessment-type tools              |

### 5.4 Reporting

| Req ID  | Requirement                                                              |
|---------|--------------------------------------------------------------------------|
| FR-016  | System SHALL generate HTML reports for assessment tool results           |
| FR-017  | Reports SHALL include timestamp, tool name, target, and parsed findings  |
| FR-018  | Reports SHALL be exportable / saveable to disk                           |

---

## 6. Non-Functional Requirements

| Req ID  | Category        | Requirement                                                        |
|---------|-----------------|--------------------------------------------------------------------|
| NFR-001 | Performance     | GUI SHALL remain responsive during tool execution                  |
| NFR-002 | Reliability     | System SHALL not crash on unexpected tool output                   |
| NFR-003 | Compatibility   | System SHALL work on default Kali Linux installations              |
| NFR-004 | Portability      | System SHALL NOT modify any Kali system binaries                   |
| NFR-005 | Installability  | System SHALL install cleanly via `sudo dpkg -i kalinova.deb`      |
| NFR-006 | Uninstallability| System SHALL uninstall cleanly via `sudo dpkg -r kalinova`        |
| NFR-007 | Usability       | System SHALL be usable without any terminal knowledge              |
| NFR-008 | Safety          | System SHALL include a legal disclaimer on first launch            |
| NFR-009 | Maintainability | Adding a new tool SHALL NOT require modifying core application code|

---

## 7. Constraints

| Constraint                   | Description                                                         |
|------------------------------|---------------------------------------------------------------------|
| Platform                     | Kali Linux only (Debian-based)                                     |
| Language                     | Python 3.x                                                          |
| GUI Framework                | PyQt6                                                               |
| ML Framework                 | scikit-learn with joblib serialization                              |
| Tool Execution               | QProcess (no subprocess or os.system)                              |
| Installation Path            | `/opt/kalinova`                                                     |
| Desktop Integration          | `/usr/share/applications/`                                         |
| MVP Tool Count               | 4 tools initially (Nmap, Nikto, John, Hydra) — scaling to 600+    |

---

## 8. Assumptions

1. Users have Kali Linux installed with default tool packages.
2. Supported tools are pre-installed on the target system (MVP: Nmap, Nikto, John, Hydra).
3. Users have basic understanding of networking concepts (IP, ports).
4. The ML model is pre-trained offline and bundled with the .deb package.
5. Internet connectivity is NOT required for core functionality.

---

## 9. Success Metrics

| Metric                              | Target                                    |
|--------------------------------------|-------------------------------------------|
| Terminal Usage Required              | 0 (zero CLI interactions needed)          |
| Tool Execution Stability             | < 2% crash rate during tool execution     |
| ML Prediction Accuracy              | > 70% on test dataset                    |
| Installation / Uninstallation        | Clean, no residual files                  |
| Beginner Usability Score             | > 4.0 / 5.0 in usability testing         |
| Report Generation Success Rate       | 100% for assessment tools                 |

---

## 10. Risks & Mitigations

| Risk                                 | Impact   | Probability | Mitigation                                   |
|--------------------------------------|----------|-------------|----------------------------------------------|
| Poor ML dataset quality              | High     | Medium      | Use controlled synthetic + real-world data   |
| Tool output format changes upstream  | Medium   | Low         | Modular parsers, version-pinned tool support |
| Overengineering the UI               | Medium   | Medium      | Strict MVP scope, iterative design           |
| QProcess compatibility issues        | High     | Low         | Comprehensive testing on Kali variants       |
| User misuse for unauthorized testing | High     | Medium      | Legal disclaimer, ethical usage guidelines   |

---

## 11. Release Criteria (MVP)

- [ ] All MVP tool GUIs functional (Nmap, Nikto, John, Hydra)
- [ ] Plugin architecture validated — new tool addable without core changes
- [ ] Terminal-free execution verified
- [ ] Parsers produce correct structured output for all tools
- [ ] Tool-type adaptive output working for all 3 types
- [ ] ML model loaded and predictions displayed with confidence
- [ ] HTML report generation for assessment tools
- [ ] .deb package builds and installs cleanly
- [ ] Clean uninstallation verified
- [ ] Legal disclaimer displayed on first launch
- [ ] No modification to Kali system files confirmed
