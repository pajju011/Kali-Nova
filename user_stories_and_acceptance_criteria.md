# Kalinova — User Stories & Acceptance Criteria

**Version:** 1.0  
**Date:** 2026-03-03  
**Status:** Draft  

---

## Overview

This document defines all user stories for the Kalinova project, organized by epics. The MVP begins with 4 tools (Nmap, Nikto, John, Hydra) but Kalinova is designed to **scale to all 600+ Kali Linux tools** over time. Each story follows the standard format and includes detailed acceptance criteria using the Given-When-Then pattern.

---

## Epic 1: Dashboard & Navigation

### US-1.1: View Central Dashboard

**As a** cybersecurity student,  
**I want to** see a central dashboard when I open Kalinova,  
**So that** I can quickly select and launch the security tool I need.

**Acceptance Criteria:**

| # | Given | When | Then |
|---|-------|------|------|
| 1 | The user has installed Kalinova | The user launches the application | A central dashboard is displayed showing all registered tools (MVP: Nmap, Nikto, John, Hydra; scales to 600+) |
| 2 | The dashboard is visible | The user views the dashboard | Each tool is represented with a clickable card/button with name and icon |
| 3 | The dashboard is visible | The user views the dashboard | The tool type (Assessment / Action / Utility) is indicated for each tool |
| 4 | New tools are added post-MVP | The user launches the application | Newly registered tools automatically appear on the dashboard |

---

### US-1.2: Navigate to Tool Window

**As a** beginner ethical hacker,  
**I want to** click on a tool card to open its dedicated GUI window,  
**So that** I can configure and run that tool without using the terminal.

**Acceptance Criteria:**

| # | Given | When | Then |
|---|-------|------|------|
| 1 | The dashboard is displayed | The user clicks on the Nmap card | The Nmap GUI window opens with input fields (target IP, scan type, etc.) |
| 2 | The dashboard is displayed | The user clicks on the Nikto card | The Nikto GUI window opens with input fields (target URL, options) |
| 3 | The dashboard is displayed | The user clicks on the John card | The John GUI window opens with input fields (hash file, wordlist) |
| 4 | The dashboard is displayed | The user clicks on the Hydra card | The Hydra GUI window opens with input fields (target, service, credentials) |
| 5 | A tool window is open | The user clicks the back/home button | The dashboard is displayed again |

---

## Epic 2: Tool Execution

### US-2.1: Execute Nmap Scan

**As a** cybersecurity student,  
**I want to** run an Nmap scan by filling in a form and clicking "Scan",  
**So that** I can discover open ports and services without typing any CLI commands.

**Acceptance Criteria:**

| # | Given | When | Then |
|---|-------|------|------|
| 1 | Nmap GUI is open | The user enters a valid target IP and selects scan type | The "Scan" button becomes active |
| 2 | Valid inputs are provided | The user clicks "Scan" | Nmap executes in the background via QProcess with no visible terminal |
| 3 | Nmap is running | The user views the UI | A loading/progress indicator is displayed |
| 4 | Nmap completes successfully | The output is returned | Parsed, structured results are displayed in the results panel |
| 5 | Nmap is running | The user clicks "Cancel" | The Nmap process is terminated and a cancellation message is shown |

---

### US-2.2: Execute Nikto Scan

**As a** cybersecurity student,  
**I want to** run a Nikto web vulnerability scan via the GUI,  
**So that** I can identify web server vulnerabilities without CLI knowledge.

**Acceptance Criteria:**

| # | Given | When | Then |
|---|-------|------|------|
| 1 | Nikto GUI is open | The user enters a valid target URL | The "Scan" button becomes active |
| 2 | Valid inputs are provided | The user clicks "Scan" | Nikto executes in the background via QProcess |
| 3 | Nikto completes successfully | Results are returned | Parsed vulnerability findings are displayed with severity classification |
| 4 | Nikto fails or returns errors | The error is captured | A friendly, non-technical error message is displayed |

---

### US-2.3: Execute John the Ripper

**As a** beginner ethical hacker,  
**I want to** run John the Ripper for password hash cracking via a GUI,  
**So that** I can learn about password security without CLI complexity.

**Acceptance Criteria:**

| # | Given | When | Then |
|---|-------|------|------|
| 1 | John GUI is open | The user selects a hash file and optionally a wordlist | The "Crack" button becomes active |
| 2 | Valid inputs are provided | The user clicks "Crack" | John executes in the background via QProcess |
| 3 | John completes | Results are returned | Cracked passwords are displayed in a structured summary format |
| 4 | John is running | The user clicks "Cancel" | The process is terminated gracefully |

---

### US-2.4: Execute Hydra

**As a** beginner ethical hacker,  
**I want to** run Hydra for brute-force login testing via a GUI,  
**So that** I can understand credential attacks without memorizing CLI flags.

**Acceptance Criteria:**

| # | Given | When | Then |
|---|-------|------|------|
| 1 | Hydra GUI is open | The user enters target, service, username, and password list | The "Attack" button becomes active |
| 2 | Valid inputs are provided | The user clicks "Attack" | Hydra executes in the background via QProcess |
| 3 | Hydra completes | Results are returned | Successful credentials are displayed in a structured summary |
| 4 | Hydra encounters an error | The error is captured | A friendly error message is shown (e.g., "Target unreachable") |

---

## Epic 3: Output Parsing & Adaptive Display

### US-3.1: View Structured Assessment Output

**As a** cybersecurity student,  
**I want to** see Nmap/Nikto results in a structured, tabular format,  
**So that** I can understand findings without reading raw terminal output.

**Acceptance Criteria:**

| # | Given | When | Then |
|---|-------|------|------|
| 1 | An assessment tool (Nmap/Nikto) has completed | Results are displayed | Output shows a full structured report (tables, categorized findings) |
| 2 | Results are displayed | The user reviews findings | Each finding includes port/service, status, and risk level |

---

### US-3.2: View Structured Action Output

**As a** beginner ethical hacker,  
**I want to** see John/Hydra results as a concise summary,  
**So that** I can quickly see which credentials were found.

**Acceptance Criteria:**

| # | Given | When | Then |
|---|-------|------|------|
| 1 | An action tool (John/Hydra) has completed | Results are displayed | Output shows a structured summary (not a full report) |
| 2 | Results are displayed | The user reviews findings | Cracked credentials are listed clearly |

---

### US-3.3: Tool-Type Adaptive Formatting

**As a** user,  
**I want** the output display to automatically adapt based on the tool type,  
**So that** I get the most appropriate visualization for each tool's results.

**Acceptance Criteria:**

| # | Given | When | Then |
|---|-------|------|------|
| 1 | Any tool has completed | The system determines the tool type | Assessment tools → full report; Action tools → summary; Utility tools → formatted text |
| 2 | A tool type is declared | The output is rendered | No manual configuration is needed by the user |

---

## Epic 4: ML-Powered Suggestions

### US-4.1: Receive Next-Step Suggestion

**As a** cybersecurity student,  
**I want to** receive an intelligent suggestion for what tool to use next after an assessment scan,  
**So that** I can follow a guided workflow without prior expertise.

**Acceptance Criteria:**

| # | Given | When | Then |
|---|-------|------|------|
| 1 | An assessment tool (Nmap/Nikto) has completed | Parsed results are available | The ML engine extracts features from the results |
| 2 | Features are extracted | The ML model runs prediction | A recommended next tool is displayed in the suggestion panel |
| 3 | A suggestion is displayed | The user views the suggestion | The confidence percentage is shown alongside the recommendation |
| 4 | A suggestion is displayed | The user clicks on the suggestion | The recommended tool's GUI window opens with relevant context |

---

### US-4.2: Confidence Score Display

**As a** user,  
**I want to** see the confidence level of each ML suggestion,  
**So that** I can decide whether to follow the recommendation.

**Acceptance Criteria:**

| # | Given | When | Then |
|---|-------|------|------|
| 1 | ML prediction is made | Confidence is calculated | Confidence is displayed as a percentage (e.g., "85% confident") |
| 2 | Confidence is below 50% | The suggestion is displayed | A warning indicator is shown (e.g., "Low confidence") |
| 3 | Confidence is above 70% | The suggestion is displayed | The suggestion is highlighted as "Recommended" |

---

## Epic 5: Reporting

### US-5.1: Generate HTML Report

**As a** cybersecurity student,  
**I want to** generate an HTML report from my assessment scan results,  
**So that** I can submit it for coursework or share with my team.

**Acceptance Criteria:**

| # | Given | When | Then |
|---|-------|------|------|
| 1 | An assessment tool has completed | The user clicks "Export Report" | An HTML report is generated and saved to disk |
| 2 | Report is generated | The user opens the report | It contains: timestamp, tool name, target, parsed findings, and risk classification |
| 3 | An action tool has completed | The user checks for report option | Report export is NOT available (action tools only produce summaries) |

---

## Epic 6: Beginner Support

### US-6.1: View Tool Explanations

**As a** beginner ethical hacker,  
**I want to** see a plain-language explanation of what each tool does,  
**So that** I can learn while using the application.

**Acceptance Criteria:**

| # | Given | When | Then |
|---|-------|------|------|
| 1 | A tool GUI is open | The user views the window | A brief explanation panel describes what the tool does and common use cases |
| 2 | An assessment completes | Results are displayed | Key findings include beginner-friendly explanations (e.g., "Port 22 (SSH) is open — this allows remote login") |

---

### US-6.2: Risk Classification

**As a** cybersecurity student,  
**I want** findings to be classified by risk level,  
**So that** I can prioritize what to investigate first.

**Acceptance Criteria:**

| # | Given | When | Then |
|---|-------|------|------|
| 1 | An assessment tool has completed | Results are parsed | Each finding is tagged with a risk level: Critical / High / Medium / Low / Info |
| 2 | Results are displayed | The user views findings | Risk levels are visually distinct (color-coded or icon-based) |

---

## Epic 7: Installation & Deployment

### US-7.1: Install Kalinova

**As a** user,  
**I want to** install Kalinova using a standard .deb package,  
**So that** I can set it up with a single command.

**Acceptance Criteria:**

| # | Given | When | Then |
|---|-------|------|------|
| 1 | The user has the .deb file | The user runs `sudo dpkg -i kalinova.deb` | Kalinova is installed to `/opt/kalinova` |
| 2 | Installation completes | The user checks applications menu | A Kalinova desktop entry appears in the applications menu |
| 3 | Installation completes | The user verifies system state | No Kali system files have been modified |

---

### US-7.2: Uninstall Kalinova

**As a** user,  
**I want to** completely remove Kalinova from my system,  
**So that** no residual files or configurations remain.

**Acceptance Criteria:**

| # | Given | When | Then |
|---|-------|------|------|
| 1 | Kalinova is installed | The user runs `sudo dpkg -r kalinova` | All Kalinova files are removed from `/opt/kalinova` |
| 2 | Removal completes | The user checks | Desktop entries are removed |
| 3 | Removal completes | The user verifies system state | No residual configuration files remain |

---

## Epic 8: Legal & Safety

### US-8.1: Legal Disclaimer

**As a** user,  
**I want to** see a legal disclaimer on first launch,  
**So that** I understand the ethical and legal boundaries of using security tools.

**Acceptance Criteria:**

| # | Given | When | Then |
|---|-------|------|------|
| 1 | The user launches Kalinova for the first time | The application starts | A legal disclaimer dialog is displayed |
| 2 | The disclaimer is shown | The user accepts the terms | The dashboard is displayed |
| 3 | The disclaimer is shown | The user declines | The application exits gracefully |

---

## Epic 9: Tool Scalability & Expansion

### US-9.1: Add New Tool via Plugin

**As a** developer/contributor,  
**I want to** add a new Kali Linux tool to Kalinova without modifying core code,  
**So that** the tool library can grow towards covering all 600+ Kali tools.

**Acceptance Criteria:**

| # | Given | When | Then |
|---|-------|------|------|
| 1 | A new tool definition file (YAML/JSON) is created | The application starts | The new tool appears on the dashboard automatically |
| 2 | A new parser class is registered | A scan completes | The output is parsed and displayed correctly |
| 3 | No core files are modified | The new tool is used | All existing tools continue to work without regression |

### US-9.2: Browse Categorized Tool Library

**As a** cybersecurity student,  
**I want to** browse tools organized by Kali Linux categories (Information Gathering, Vulnerability Analysis, Web Applications, etc.),  
**So that** I can find the right tool for my task even as the library grows to hundreds of tools.

**Acceptance Criteria:**

| # | Given | When | Then |
|---|-------|------|------|
| 1 | 20+ tools are registered | The user views the dashboard | Tools are grouped by Kali category |
| 2 | The user selects a category | The dashboard filters | Only tools in that category are displayed |
| 3 | The user searches for a tool | The search runs | Matching tools are shown regardless of category |

### US-9.3: Auto-Detect Available Tools

**As a** user,  
**I want** Kalinova to automatically detect which Kali tools are installed on my system,  
**So that** the dashboard only shows tools I can actually use.

**Acceptance Criteria:**

| # | Given | When | Then |
|---|-------|------|------|
| 1 | Kalinova launches | The tool registry loads | Each tool's CLI binary is checked for availability |
| 2 | A tool is not installed | The dashboard displays | The tool card shows "Not Installed" with install instructions |
| 3 | A tool is installed | The dashboard displays | The tool card is fully active and launchable |

---

## Story Map Summary

| Epic                           | Stories | Priority |
|--------------------------------|---------|----------|
| Dashboard & Navigation         | 2       | P0       |
| Tool Execution                 | 4       | P0       |
| Output Parsing & Display       | 3       | P0       |
| ML-Powered Suggestions         | 2       | P0-P1    |
| Reporting                      | 1       | P1       |
| Beginner Support               | 2       | P1       |
| Installation & Deployment      | 2       | P0       |
| Legal & Safety                 | 1       | P0       |
| Tool Scalability & Expansion   | 3       | P1-P2    |
| **Total**                      | **20**  |          |
