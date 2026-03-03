# Kalinova — Development Phases

**Version:** 1.0 | **Date:** 2026-03-03

---

## 1. Overview

Kalinova follows a **multi-phase incremental development** approach. The initial 4 phases deliver the MVP. Subsequent phases continuously expand the tool library towards **covering all 600+ Kali Linux tools**. Each phase delivers a working increment that can be tested independently.

---

## 2. Phase 1 — Foundation (Weeks 1-3)

### Objective
Set up project infrastructure, build the core execution engine, and create the dashboard shell.

### Deliverables

| ID   | Task                                   | Est. Effort | Priority |
|------|----------------------------------------|-------------|----------|
| P1.1 | Project scaffolding (monorepo setup)  | 4 hrs       | P0       |
| P1.2 | Python environment + requirements.txt | 2 hrs       | P0       |
| P1.3 | ProcessRunner (QProcess wrapper)      | 12 hrs      | P0       |
| P1.4 | CommandBuilder module                 | 8 hrs       | P0       |
| P1.5 | Tool Registry + BaseTool interface    | 4 hrs       | P0       |
| P1.6 | Exception hierarchy                   | 2 hrs       | P0       |
| P1.7 | Dashboard window (shell, no tools)    | 8 hrs       | P0       |
| P1.8 | Disclaimer dialog                     | 4 hrs       | P1       |
| P1.9 | Dark theme stylesheet                 | 4 hrs       | P1       |
| P1.10| Unit tests for core modules           | 6 hrs       | P0       |
| P1.11| CI pipeline setup (.github/workflows) | 4 hrs       | P1       |

### Exit Criteria
- [ ] ProcessRunner can execute a CLI tool and capture output
- [ ] CommandBuilder correctly constructs commands from params
- [ ] Dashboard window launches with placeholder cards
- [ ] Disclaimer dialog shows on first launch
- [ ] All unit tests pass
- [ ] CI pipeline runs lint + tests on push

---

## 3. Phase 2 — Core Tools (Weeks 4-7)

### Objective
Build all 4 tool GUIs, parsers, and the tool-type handler layer.

### Deliverables

| ID   | Task                                   | Est. Effort | Priority |
|------|----------------------------------------|-------------|----------|
| P2.1 | BaseToolWindow abstract class         | 4 hrs       | P0       |
| P2.2 | Nmap GUI window                       | 8 hrs       | P0       |
| P2.3 | Nmap parser                           | 6 hrs       | P0       |
| P2.4 | Nikto GUI window                      | 8 hrs       | P0       |
| P2.5 | Nikto parser                          | 6 hrs       | P0       |
| P2.6 | John GUI window                       | 6 hrs       | P0       |
| P2.7 | John parser                           | 6 hrs       | P0       |
| P2.8 | Hydra GUI window                      | 6 hrs       | P0       |
| P2.9 | Hydra parser                          | 6 hrs       | P0       |
| P2.10| Tool-type handler (output routing)    | 8 hrs       | P0       |
| P2.11| Risk classifier module                | 4 hrs       | P1       |
| P2.12| Results panel widget                  | 8 hrs       | P0       |
| P2.13| Input validation for all tools        | 4 hrs       | P0       |
| P2.14| Dashboard integration (real tool cards)| 4 hrs      | P0       |
| P2.15| Unit tests for parsers + handlers     | 8 hrs       | P0       |
| P2.16| Integration test: end-to-end scan     | 6 hrs       | P0       |

### Exit Criteria
- [ ] All 4 tools can be launched from dashboard
- [ ] Each tool accepts inputs, executes, and displays parsed results
- [ ] Assessment tools show full structured reports
- [ ] Action tools show structured summaries
- [ ] All parsers handle typical output formats correctly
- [ ] Cancel functionality works for all tools
- [ ] All unit + integration tests pass

---

## 4. Phase 3 — ML Engine & Reporting (Weeks 8-9)

### Objective
Build the ML scoring engine, suggestion panel, and report generation.

### Deliverables

| ID   | Task                                   | Est. Effort | Priority |
|------|----------------------------------------|-------------|----------|
| P3.1 | Feature extractor (Nmap)              | 6 hrs       | P0       |
| P3.2 | Feature extractor (Nikto)             | 6 hrs       | P0       |
| P3.3 | Training data generation script       | 8 hrs       | P0       |
| P3.4 | Model training script                 | 4 hrs       | P0       |
| P3.5 | Model evaluation + validation         | 4 hrs       | P0       |
| P3.6 | Predictor module (load + predict)     | 6 hrs       | P0       |
| P3.7 | Confidence scorer                     | 2 hrs       | P0       |
| P3.8 | Suggestion panel widget               | 6 hrs       | P0       |
| P3.9 | Report HTML template                  | 4 hrs       | P1       |
| P3.10| Report generator module               | 6 hrs       | P1       |
| P3.11| Report viewer dialog                  | 4 hrs       | P1       |
| P3.12| ML unit tests                         | 4 hrs       | P0       |
| P3.13| ML integration test                   | 4 hrs       | P0       |

### Exit Criteria
- [ ] ML model trained with >70% accuracy
- [ ] Suggestion panel displays after assessment scans
- [ ] Confidence scores are accurate and labeled correctly
- [ ] HTML reports generate correctly for Nmap and Nikto
- [ ] Reports are saveable to disk
- [ ] All ML tests pass

---

## 5. Phase 4 — Polish, Packaging & QA (Weeks 10-11)

### Objective
Final UI polish, .deb packaging, comprehensive testing, and documentation.

### Deliverables

| ID   | Task                                   | Est. Effort | Priority |
|------|----------------------------------------|-------------|----------|
| P4.1 | UI polish (animations, loading states)| 8 hrs       | P1       |
| P4.2 | Beginner explanation panel content    | 4 hrs       | P1       |
| P4.3 | Error message improvements            | 4 hrs       | P1       |
| P4.4 | SQLite history storage                | 6 hrs       | P2       |
| P4.5 | .deb package build script             | 4 hrs       | P0       |
| P4.6 | Desktop entry file                    | 2 hrs       | P0       |
| P4.7 | Install/uninstall testing             | 4 hrs       | P0       |
| P4.8 | End-to-end test suite                 | 8 hrs       | P0       |
| P4.9 | Performance testing                   | 4 hrs       | P1       |
| P4.10| Security review                       | 4 hrs       | P1       |
| P4.11| User documentation                    | 6 hrs       | P1       |
| P4.12| Final bug fixes                       | 8 hrs       | P0       |

### Exit Criteria
- [ ] Application is visually polished and responsive
- [ ] .deb package builds successfully
- [ ] Clean install + uninstall verified on fresh Kali
- [ ] E2E tests pass for all 4 tools
- [ ] No critical/high bugs remaining
- [ ] User documentation complete
- [ ] README with quickstart guide

---

## 6. Phase Summary

| Phase | Focus              | Duration | Key Output                           |
|-------|--------------------|----------|--------------------------------------|
| 1     | Foundation         | 3 weeks  | Core engine + dashboard shell       |
| 2     | Core Tools         | 4 weeks  | 4 tool GUIs + parsers + handlers    |
| 3     | ML & Reporting     | 2 weeks  | Scoring engine + reports            |
| 4     | Polish & Packaging | 2 weeks  | .deb package + QA + docs            |
| 5+    | Tool Expansion     | Ongoing  | Continuously add tools towards 600+ |
| **MVP Total** |            | **11 weeks** | **Production-ready MVP**        |

> **Post-MVP:** Phases 5+ focus on rapidly expanding the tool library. With the plugin system in place, adding each new tool takes significantly less effort (~4-8 hrs per tool including GUI, parser, and tests).

---

## 7. Post-MVP: Tool Expansion Roadmap

| Phase   | Target Tools | Categories Added                                      | Est. Per Tool |
|---------|-------------|-------------------------------------------------------|---------------|
| Phase 5 | 10-15 more  | Web Apps (Dirb, Gobuster, sqlmap), Wireless (Aircrack) | 8 hrs         |
| Phase 6 | 30-50 total | Exploitation (Metasploit CLI), Forensics, OSINT        | 6 hrs         |
| Phase 7 | 100+ total  | All major Kali categories covered                      | 4 hrs         |
| Phase 8+| 300-600+    | Full Kali tool coverage via community contributions    | 2-4 hrs       |

> As the plugin system matures, tool addition becomes primarily a **configuration task** (YAML definition + parser), drastically reducing per-tool effort.

---

## 7. Dependencies Between Phases

```
Phase 1 (Foundation)
    │
    ├── ProcessRunner ────────────────────┐
    ├── CommandBuilder ──────────────────┐│
    ├── Tool Registry ─────────────────┐││
    └── Dashboard Shell               │││
                                      │││
Phase 2 (Core Tools)                  │││
    │                                 │││
    ├── Tool GUIs ◄───────────────────┘││
    ├── Parsers ◄──────────────────────┘│
    ├── Type Handler                    │
    └── Results Panel ◄─────────────────┘
                 │
Phase 3 (ML & Reports)
    │
    ├── Feature Extractor ◄── Parsers (Phase 2)
    ├── ML Model / Predictor
    ├── Suggestion Panel ◄── Results Panel (Phase 2)
    └── Report Generator ◄── Parsers (Phase 2)
                 │
Phase 4 (Polish & Packaging)
    │
    ├── UI Polish ◄── All GUI components (Phase 1-3)
    ├── .deb Package ◄── All source code (Phase 1-3)
    └── E2E Testing ◄── All features (Phase 1-3)
```

---

## 8. Sprint Cadence

| Sprint    | Duration | Phase Mapping                     |
|-----------|----------|-----------------------------------|
| Sprint 1  | 2 weeks  | Phase 1 (Foundation - Part 1)    |
| Sprint 2  | 1 week   | Phase 1 (Foundation - Part 2)    |
| Sprint 3  | 2 weeks  | Phase 2 (Assessment Tools)       |
| Sprint 4  | 2 weeks  | Phase 2 (Action Tools + Handler) |
| Sprint 5  | 2 weeks  | Phase 3 (ML + Reporting)         |
| Sprint 6  | 2 weeks  | Phase 4 (Polish + Packaging)     |
