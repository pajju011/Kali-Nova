# Kalinova System Design Document

## 1. High-Level Flow

User
↓
Tool GUI
↓
QProcess Execution
↓
CLI Tool (Hidden)
↓
Parser
↓
Tool-Type Handler
↓
(Optional ML Prediction)
↓
Result Display / Report Generation

---

## 2. Component Design

### 2.1 BaseTool Class
Responsibilities:
- Build command
- Execute tool
- Capture output
- Handle exit status

### 2.2 Process Runner
- Wraps QProcess
- Handles signals
- Provides cancellation
- Emits structured output

### 2.3 Parser Module
Each tool has a parser returning structured data.

Example:
{
  "http": 1,
  "ssh": 0,
  "open_ports": 2
}

### 2.4 Tool-Type Handler
Defines output behavior:

assessment → full report  
action → structured result  
utility → basic formatted output  

### 2.5 ML Predictor
- Loads .pkl model
- Receives extracted features
- Returns recommended next tool + confidence

### 2.6 Report Generator
Generates HTML report for assessment tools only.

---

## 3. Scalability

To add a new tool:
1. Create GUI
2. Create parser
3. Declare tool_type
4. Register in dashboard

No core modification required.

---

## 4. Security & Safety

- No modification of Kali binaries
- No forced privilege escalation
- Legal disclaimer included
- Fully uninstallable

---

## 5. Deployment Model

Distributed as .deb package:
- Installed to /opt/kalinova
- Adds desktop entries
- Safe removal using dpkg -r