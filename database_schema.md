# Kalinova — Database Schema Document

**Version:** 1.0 | **Date:** 2026-03-03

> **Scalability Note:** The schema is designed to support an **unlimited number of tools**. The `tool_name` field in the `scans` table is a free-text reference to any tool in the dynamic registry — it is not limited to MVP tools.

---

## 1. Overview

Kalinova is a desktop application that operates **without a traditional database server**. Data persistence is handled via **local file-based storage** using JSON files and SQLite for session/history management. This document defines all data schemas used across the application.

---

## 2. Storage Strategy

| Data Type               | Storage Method | Location                          |
|-------------------------|----------------|-----------------------------------|
| Application Config      | JSON file      | `/opt/kalinova/config/app.json`   |
| User Preferences        | JSON file      | `~/.kalinova/preferences.json`    |
| Scan History            | SQLite DB      | `~/.kalinova/history.db`          |
| ML Model                | Pickle (.pkl)  | `/opt/kalinova/models/`           |
| Generated Reports       | HTML files     | `~/.kalinova/reports/`            |
| First Launch Flag       | JSON file      | `~/.kalinova/state.json`          |

---

## 3. SQLite Schema — Scan History

### 3.1 Table: `scans`

| Column         | Type         | Constraints           | Description                               |
|----------------|--------------|-----------------------|-------------------------------------------|
| `id`           | INTEGER      | PRIMARY KEY AUTOINCR  | Unique scan identifier                    |
| `tool_name`    | TEXT         | NOT NULL              | e.g., "nmap", "nikto"                     |
| `tool_type`    | TEXT         | NOT NULL              | "assessment" / "action" / "utility"       |
| `target`       | TEXT         | NOT NULL              | Target IP/URL/file                        |
| `parameters`   | TEXT         | NULL                  | JSON string of CLI options used           |
| `raw_output`   | TEXT         | NULL                  | Raw CLI stdout                            |
| `parsed_data`  | TEXT         | NULL                  | JSON string of parsed structured output   |
| `status`       | TEXT         | NOT NULL DEFAULT 'completed' | "completed"/"cancelled"/"error"     |
| `exit_code`    | INTEGER      | NULL                  | Process exit code                         |
| `started_at`   | DATETIME     | NOT NULL              | Scan start timestamp                      |
| `completed_at` | DATETIME     | NULL                  | Scan completion timestamp                 |
| `duration_ms`  | INTEGER      | NULL                  | Execution duration in milliseconds        |
| `created_at`   | DATETIME     | DEFAULT CURRENT_TIMESTAMP | Record creation time                  |

```sql
CREATE TABLE scans (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_name     TEXT NOT NULL,
    tool_type     TEXT NOT NULL CHECK(tool_type IN ('assessment','action','utility')),
    target        TEXT NOT NULL,
    parameters    TEXT,
    raw_output    TEXT,
    parsed_data   TEXT,
    status        TEXT NOT NULL DEFAULT 'completed' CHECK(status IN ('completed','cancelled','error')),
    exit_code     INTEGER,
    started_at    DATETIME NOT NULL,
    completed_at  DATETIME,
    duration_ms   INTEGER,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 3.2 Table: `findings`

| Column         | Type         | Constraints           | Description                               |
|----------------|--------------|-----------------------|-------------------------------------------|
| `id`           | INTEGER      | PRIMARY KEY AUTOINCR  | Unique finding identifier                 |
| `scan_id`      | INTEGER      | FK → scans.id         | Associated scan                           |
| `description`  | TEXT         | NOT NULL              | Finding description                       |
| `severity`     | TEXT         | NOT NULL              | "critical"/"high"/"medium"/"low"/"info"   |
| `category`     | TEXT         | NULL                  | e.g., "open_port", "vulnerability"        |
| `details`      | TEXT         | NULL                  | JSON string with additional details       |
| `created_at`   | DATETIME     | DEFAULT CURRENT_TIMESTAMP | Record creation time                  |

```sql
CREATE TABLE findings (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id       INTEGER NOT NULL,
    description   TEXT NOT NULL,
    severity      TEXT NOT NULL CHECK(severity IN ('critical','high','medium','low','info')),
    category      TEXT,
    details       TEXT,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scan_id) REFERENCES scans(id) ON DELETE CASCADE
);
```

### 3.3 Table: `suggestions`

| Column            | Type         | Constraints           | Description                            |
|-------------------|--------------|-----------------------|----------------------------------------|
| `id`              | INTEGER      | PRIMARY KEY AUTOINCR  | Unique suggestion identifier           |
| `scan_id`         | INTEGER      | FK → scans.id         | Associated scan                        |
| `recommended_tool`| TEXT         | NOT NULL              | Suggested next tool name               |
| `confidence`      | REAL         | NOT NULL              | Confidence score (0.0 - 1.0)           |
| `confidence_label`| TEXT         | NOT NULL              | "high" / "medium" / "low"             |
| `features_used`   | TEXT         | NULL                  | JSON string of feature vector          |
| `accepted`        | BOOLEAN      | DEFAULT 0             | Whether user followed suggestion       |
| `created_at`      | DATETIME     | DEFAULT CURRENT_TIMESTAMP | Record creation time               |

```sql
CREATE TABLE suggestions (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id           INTEGER NOT NULL,
    recommended_tool  TEXT NOT NULL,
    confidence        REAL NOT NULL,
    confidence_label  TEXT NOT NULL CHECK(confidence_label IN ('high','medium','low')),
    features_used     TEXT,
    accepted          BOOLEAN DEFAULT 0,
    created_at        DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scan_id) REFERENCES scans(id) ON DELETE CASCADE
);
```

### 3.4 Table: `reports`

| Column         | Type         | Constraints           | Description                               |
|----------------|--------------|-----------------------|-------------------------------------------|
| `id`           | INTEGER      | PRIMARY KEY AUTOINCR  | Unique report identifier                  |
| `scan_id`      | INTEGER      | FK → scans.id         | Associated scan                           |
| `file_path`    | TEXT         | NOT NULL              | Path to generated HTML file               |
| `generated_at` | DATETIME     | NOT NULL              | Report generation timestamp               |

```sql
CREATE TABLE reports (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id       INTEGER NOT NULL,
    file_path     TEXT NOT NULL,
    generated_at  DATETIME NOT NULL,
    FOREIGN KEY (scan_id) REFERENCES scans(id) ON DELETE CASCADE
);
```

---

## 4. JSON Schemas

### 4.1 Application Config (`app.json`)

```json
{
    "version": "1.0.0",
    "install_path": "/opt/kalinova",
    "auto_discover_tools": true,
    "tool_plugins_dir": "/opt/kalinova/plugins/tools/",
    "tools": {
        "nmap": {"path": "/usr/bin/nmap", "enabled": true, "category": "information_gathering"},
        "nikto": {"path": "/usr/bin/nikto", "enabled": true, "category": "vulnerability_analysis"},
        "john": {"path": "/usr/sbin/john", "enabled": true, "category": "password_attacks"},
        "hydra": {"path": "/usr/bin/hydra", "enabled": true, "category": "password_attacks"}
    },
    "ml_model_path": "/opt/kalinova/models/next_tool_model.pkl",
    "report_template": "/opt/kalinova/reports/templates/report_template.html"
}
```

### 4.2 User Preferences (`preferences.json`)

```json
{
    "theme": "dark",
    "default_scan_type": "SYN",
    "auto_export_reports": false,
    "report_output_dir": "~/kalinova-reports",
    "show_beginner_tips": true,
    "ml_suggestions_enabled": true
}
```

### 4.3 Application State (`state.json`)

```json
{
    "first_launch_completed": true,
    "disclaimer_accepted": true,
    "disclaimer_accepted_at": "2026-03-03T11:30:00Z",
    "last_opened": "2026-03-03T11:40:00Z",
    "total_scans_run": 42
}
```

---

## 5. Entity Relationship Diagram

```
┌──────────┐       ┌──────────────┐
│  scans   │──1:N──│  findings    │
│          │       └──────────────┘
│          │       ┌──────────────┐
│          │──1:N──│ suggestions  │
│          │       └──────────────┘
│          │       ┌──────────────┐
│          │──1:1──│  reports     │
└──────────┘       └──────────────┘
```

---

## 6. Data Retention

| Data Type       | Retention Policy                           |
|-----------------|---------------------------------------------|
| Scan History    | Retained until user manually clears          |
| Reports         | Retained indefinitely (user-managed)         |
| Raw Output      | Stored with scan record                      |
| ML Suggestions  | Stored with scan record                      |
| Preferences     | Persistent across sessions                   |
