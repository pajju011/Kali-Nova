# Kalinova — Engineering Scope Definition

**Version:** 1.0 | **Date:** 2026-03-03

---

## 1. Purpose

This document defines the precise engineering scope for Kalinova — what is being built, what is explicitly deferred, and the boundaries for each development phase. Kalinova's long-term vision is to provide GUI wrappers for **all 600+ Kali Linux tools**. The MVP starts with 4 tools, but all architecture decisions must support **unlimited future tool expansion**.

---

## 2. In-Scope (MVP)

### 2.1 Tool Wrappers

| Tool            | Type       | GUI | Parser | ML | Report |
|-----------------|------------|-----|--------|----|--------|
| Nmap            | Assessment | ✅  | ✅     | ✅ | ✅     |
| Nikto           | Assessment | ✅  | ✅     | ✅ | ✅     |
| John the Ripper | Action     | ✅  | ✅     | ❌ | ❌     |
| Hydra           | Action     | ✅  | ✅     | ❌ | ❌     |

### 2.2 Core Engine

| Component           | Scope                                                    |
|---------------------|----------------------------------------------------------|
| Process Runner      | QProcess wrapper with start/cancel/capture/error handling |
| Command Builder     | Construct CLI commands from GUI form inputs               |
| Tool Registry       | **Dynamic** registry of tools with type declarations — designed for plug-in tool addition |
| Parser Framework    | Base parser + MVP parsers; extensible framework for adding unlimited parsers            |
| Type Handler        | Route output based on assessment/action/utility type — works for any registered tool  |

### 2.3 ML Intelligence

| Component           | Scope                                                    |
|---------------------|----------------------------------------------------------|
| Feature Extractor   | Extract 12-15 features from Nmap & Nikto results         |
| Model               | Pre-trained Random Forest (.pkl), bundled with package   |
| Predictor           | Load model, predict next tool, return confidence         |
| Confidence Scorer   | High (≥75%), Medium (≥50%), Low (<50%)                   |

### 2.4 GUI

| Component           | Scope                                                    |
|---------------------|----------------------------------------------------------|
| Dashboard           | Tool cards, tool-type labels, navigation                 |
| Tool Windows        | Input forms with validation, execute/cancel buttons      |
| Results Panel       | Structured output display, risk badges                   |
| Suggestion Panel    | ML recommendation with confidence indicator              |
| Disclaimer Dialog   | First-launch legal consent                               |

### 2.5 Reporting

| Component           | Scope                                                    |
|---------------------|----------------------------------------------------------|
| Report Generator    | HTML report from template for assessment tools only      |
| Report Viewer       | In-app preview + save to disk                            |

### 2.6 Packaging

| Component           | Scope                                                    |
|---------------------|----------------------------------------------------------|
| .deb Package        | Build via dpkg-deb, install to /opt/kalinova             |
| Desktop Entry       | .desktop file in /usr/share/applications/                |
| Clean Uninstall     | dpkg -r removes all files cleanly                        |

---

## 3. Out of Scope (Explicitly Deferred)

| Item                          | Reason                                                | Phase    |
|-------------------------------|-------------------------------------------------------|----------|
| Full 600+ tool coverage       | MVP starts with 4; tools will be added continuously   | Ongoing  |
| Custom Kali ISO               | Requires separate distribution pipeline               | Phase 4+ |
| Cloud-based ML                | MVP uses offline model only                 | Phase 3+ |
| Multi-user management         | Desktop app, single-user context            | Phase 3+ |
| Web-based UI                  | Desktop-only (PyQt6) for MVP                | Phase 3+ |
| Automated pentest workflows   | Manual tool selection in MVP                | Phase 2  |
| Plugin/extension system       | Tool addition requires code changes in MVP  | Phase 2  |
| Scan scheduling               | Real-time execution only in MVP             | Phase 2  |
| Network topology visualization| Beyond MVP scope                            | Phase 2  |
| Custom theme engine           | Dark mode only in MVP                       | Phase 2  |
| Internationalization (i18n)   | English only in MVP                         | Phase 3+ |
| Accessibility (full WCAG)     | Basic accessibility in MVP                  | Phase 2  |

---

## 4. Engineering Boundaries

### 4.1 What Kalinova IS

- A GUI wrapper layer over existing Kali CLI tools — **designed to cover all 600+ tools over time**
- A modular, installable desktop application with a **plugin-based tool system**
- An ML-assisted suggestion engine that **scales with tool count**
- A beginner-focused tool for ethical hacking education

### 4.2 What Kalinova IS NOT

- Not a replacement for Kali Linux tools
- Not a modification of Kali system binaries
- Not a cloud service or web application
- Not a full automation framework
- Not a vulnerability management platform

---

## 5. Technical Constraints

| Constraint           | Detail                                            |
|----------------------|---------------------------------------------------|
| Language             | Python 3.10+ (no other languages in MVP)          |
| GUI Framework        | PyQt6 only (no web frameworks)                    |
| Process Execution    | QProcess only (no subprocess/os.system)            |
| ML Framework         | scikit-learn only (no TensorFlow/PyTorch)          |
| Packaging            | .deb only (no AppImage, Flatpak, Snap)             |
| Installation Path    | /opt/kalinova (non-negotiable)                     |
| System Modification  | Zero modification to Kali system files             |
| Network Requirement  | None (fully offline operation)                     |
| Storage              | SQLite + JSON files (no external databases)        |

---

## 6. Definition of Done (MVP)

An MVP feature is "done" when:

- [ ] Code is implemented and follows project style guide
- [ ] Unit tests pass with >80% coverage for the component
- [ ] Integration test passes for the feature pipeline
- [ ] GUI component is functional and visually complete
- [ ] Code review completed by at least 1 peer
- [ ] No critical or high-severity bugs remain
- [ ] Documentation updated (API contracts, user guide)
- [ ] Feature works on fresh Kali Linux installation

---

## 7. Estimation Summary

### 7.1 Effort Breakdown by Layer

| Layer                | Estimated Effort | Complexity |
|----------------------|-----------------|------------|
| GUI (Dashboard + MVP tools) | 40 hrs    | Medium     |
| Core (ProcessRunner + CommandBuilder + Plugin System) | 28 hrs | Medium-High |
| Parsers (MVP + framework)  | 28 hrs          | Medium     |
| Tool-Type Handler     | 8 hrs           | Low        |
| ML Engine             | 30 hrs          | High       |
| Reporting             | 12 hrs          | Low        |
| Packaging (.deb)      | 8 hrs           | Low        |
| Testing               | 30 hrs          | Medium     |
| Documentation         | 12 hrs          | Low        |
| **Total**             | **196 hrs**     |            |

### 7.2 Risk-Adjusted Timeline

| Milestone            | Target Duration | Buffer |
|----------------------|-----------------|--------|
| Phase 1 — Foundation | 3 weeks         | +1 wk  |
| Phase 2 — Core Tools | 4 weeks         | +1 wk  |
| Phase 3 — ML Engine  | 2 weeks         | +1 wk  |
| Phase 4 — Polish     | 2 weeks         | +1 wk  |
| **Total**            | **11 weeks**    | **+4** |
