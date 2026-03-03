# Kalinova — Information Architecture

**Version:** 1.0  
**Date:** 2026-03-03  
**Status:** Draft  

> **Note:** Kalinova is designed to scale from 4 MVP tools to **all 600+ Kali Linux tools**. The information architecture supports dynamic tool registration, category-based browsing, and search/filter capabilities.

---

## 1. Overview

This document defines the information architecture (IA) of Kalinova — how content, screens, and data are organized within the application. It covers navigation structure, screen hierarchy, content model, and user flow mappings.

---

## 2. Application Hierarchy

```
Kalinova Application
│
├── 🔐 Legal Disclaimer (First Launch Only)
│
├── 📊 Central Dashboard
│   ├── Search & Filter Bar
│   ├── Category Navigation (Kali tool categories)
│   ├── Tool Grid / Cards (dynamically populated from registry)
│   │   ├── [Information Gathering] — Nmap, ...
│   │   ├── [Vulnerability Analysis] — Nikto, ...
│   │   ├── [Password Attacks] — John, Hydra, ...
│   │   ├── [Web Applications] — (future tools)
│   │   ├── [Wireless Attacks] — (future tools)
│   │   └── [... 14+ Kali categories]
│   └── Quick Info Bar (status, recent activity)
│
├── 🛠️ Tool Windows (Per Tool)
│   ├── Input Configuration Panel
│   │   ├── Target / Host Field
│   │   ├── Tool-Specific Options
│   │   └── Execute / Cancel Buttons
│   ├── Results Panel
│   │   ├── Structured Output Display
│   │   ├── Risk Classification Tags
│   │   └── Beginner Explanation Tooltips
│   ├── Suggestion Panel (Assessment Tools Only)
│   │   ├── Recommended Next Tool
│   │   ├── Confidence Score
│   │   └── "Go to Tool" Action Button
│   └── Report Export Button (Assessment Tools Only)
│
└── 📄 Report Viewer
    ├── HTML Report Preview
    └── Save / Export Controls
```

---

## 3. Navigation Model

### 3.1 Navigation Type: **Hub-and-Spoke**

The application uses a **hub-and-spoke** navigation pattern:

- **Hub:** Central Dashboard
- **Spokes:** Individual Tool Windows

Users always return to the dashboard to select a different tool, maintaining a flat and simple navigation model ideal for beginners.

### 3.2 Navigation Flow Diagram

```
                    ┌─────────────┐
                    │   Launch    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Disclaimer │ (First Launch)
                    │   Dialog    │
                    └──────┬──────┘
                           │ Accept
                    ┌──────▼──────┐
              ┌─────┤  Dashboard  ├─────┐
              │     └──────┬──────┘     │
              │            │            │
        ┌─────▼────┐ ┌────▼─────┐ ┌────▼─────┐
        │ Nmap GUI │ │Nikto GUI │ │ John GUI │ ...
        └─────┬────┘ └────┬─────┘ └────┬─────┘
              │            │            │
         ┌────▼────┐  ┌───▼────┐  ┌───▼────┐
         │ Results │  │Results │  │Results │
         │+ Suggest│  │+Suggest│  │        │
         └─────────┘  └────────┘  └────────┘
```

---

## 4. Screen Inventory

| Screen ID | Screen Name            | Parent          | Tool Type  | Description                                                  |
|-----------|------------------------|-----------------|------------|--------------------------------------------------------------|
| S-001     | Legal Disclaimer       | Launch          | N/A        | First-launch consent dialog                                  |
| S-002     | Central Dashboard      | Root            | N/A        | Main hub — scalable grid, search, categories for 600+ tools  |
| S-003     | Tool GUI (Dynamic)     | Dashboard       | Any        | Auto-generated or custom GUI per registered tool             |
| S-004     | Results Panel          | Tool Window     | Varies     | Displays parsed, structured results                          |
| S-005     | Suggestion Panel       | Results (Assess)| Assessment | ML next-step recommendation                                  |
| S-006     | Report Viewer          | Results (Assess)| Assessment | HTML report preview and export                               |

> **MVP screens include dedicated GUIs for Nmap, Nikto, John, and Hydra.** As the tool library grows, tools can use auto-generated forms from their YAML/JSON definition files.

---

## 5. Content Model

### 5.1 Tool Entity

```
Tool
├── name: String                    (e.g., "Nmap")
├── tool_type: Enum                 (assessment | action | utility)
├── description: String             (beginner-friendly explanation)
├── icon: ImagePath                 (tool icon for dashboard)
├── cli_command: String             (e.g., "nmap")
├── supported_options: List<Option>
│   ├── option_name: String
│   ├── option_flag: String         (e.g., "-sV")
│   ├── option_description: String
│   ├── input_type: Enum            (text | select | checkbox | file)
│   └── required: Boolean
├── parser: ParserModule            (reference to parser class)
└── ml_enabled: Boolean             (whether ML suggestions apply)
```

### 5.2 Scan Result Entity

```
ScanResult
├── tool_name: String
├── tool_type: Enum
├── target: String
├── timestamp: DateTime
├── raw_output: String
├── parsed_data: Dict
│   └── (tool-specific structured data)
├── risk_findings: List<Finding>
│   ├── finding_id: String
│   ├── description: String
│   ├── severity: Enum              (Critical | High | Medium | Low | Info)
│   └── explanation: String         (beginner-friendly)
└── ml_suggestion: Suggestion | None
```

### 5.3 ML Suggestion Entity

```
Suggestion
├── recommended_tool: String
├── confidence: Float               (0.0 - 1.0)
├── confidence_label: Enum          (High | Medium | Low)
├── reasoning: String               (brief explanation)
└── context: Dict                   (features that led to this prediction)
```

### 5.4 Report Entity

```
Report
├── report_id: String
├── generated_at: DateTime
├── tool_name: String
├── target: String
├── findings: List<Finding>
├── suggestion: Suggestion | None
├── html_content: String
└── file_path: String
```

---

## 6. Information Flow

### 6.1 Assessment Tool Flow

```
User Input → CLI Execution → Raw Output → Parser → Structured Data
                                                        │
                                                ┌───────┴────────┐
                                                │                │
                                          Results Panel    Feature Extractor
                                          (Structured)          │
                                                           ML Model
                                                                │
                                                       Suggestion Panel
                                                    (Next Tool + Confidence)
                                                                │
                                                        Report Generator
                                                         (HTML Export)
```

### 6.2 Action Tool Flow

```
User Input → CLI Execution → Raw Output → Parser → Structured Data
                                                        │
                                                  Results Panel
                                                  (Summary View)
```

---

## 7. Data Taxonomy

### 7.1 Tool Types

| Type       | Behavior                          | Output Style       | ML Enabled | Report |
|------------|-----------------------------------|--------------------| -----------|--------|
| Assessment | Evaluates target state            | Full structured    | Yes        | Yes    |
| Action     | Performs an attack/operation       | Summary            | No         | No     |
| Utility    | Provides informational output     | Formatted text     | No         | No     |

### 7.2 Risk Severity Levels

| Level    | Color Code | Description                                          |
|----------|------------|------------------------------------------------------|
| Critical | 🔴 Red     | Immediate exploitation risk                          |
| High     | 🟠 Orange  | Significant vulnerability, likely exploitable        |
| Medium   | 🟡 Yellow  | Moderate risk, may require specific conditions       |
| Low      | 🔵 Blue    | Minor issue, limited impact                          |
| Info     | ⚪ Gray    | Informational finding, no direct risk                |

---

## 8. Labeling & Terminology

| Internal Term       | User-Facing Label           | Context                              |
|---------------------|-----------------------------|--------------------------------------|
| tool_type           | "Tool Category"             | Dashboard cards                      |
| assessment          | "Scanner"                   | Tool card label                      |
| action              | "Attack Tool"               | Tool card label                      |
| ml_suggestion       | "Smart Suggestion"          | Suggestion panel header              |
| confidence          | "Confidence Level"          | Suggestion panel detail              |
| parsed_data         | "Scan Results"              | Results panel header                 |
| risk_finding        | "Finding"                   | Results list item                    |
| severity            | "Risk Level"                | Finding tag                          |

---

## 9. Responsive Considerations

Since Kalinova is a desktop application (PyQt6), responsiveness refers to window resizing behavior:

| Component              | Resize Behavior                                        |
|------------------------|--------------------------------------------------------|
| Dashboard Grid         | Reflows tool cards to fit window width                 |
| Tool Input Panel       | Fixed minimum width, stretches horizontally            |
| Results Panel          | Scrollable, table columns auto-adjust                  |
| Suggestion Panel       | Fixed-height sidebar or bottom panel                   |
| Report Viewer          | Resizable with scroll                                  |

---

## 10. Accessibility Notes

| Concern               | Approach                                                |
|-----------------------|---------------------------------------------------------|
| Color-only indicators | Risk levels use both color AND text labels              |
| Keyboard navigation   | All interactive elements are tab-focusable              |
| Font sizing           | Minimum 12pt for body text, 14pt for headers           |
| Contrast              | WCAG AA compliance for text/background contrast         |
| Screen readers        | Qt accessibility labels on all interactive widgets      |
