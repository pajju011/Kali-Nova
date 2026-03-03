"""
Database — SQLite storage for scan history and findings.

Stores scan history, findings, suggestions, and reports
for session management and historical reference.
"""

import os
import sqlite3
import json
import logging
from datetime import datetime
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)


class Database:
    """
    SQLite database for Kalinova local data storage.

    Manages scan history, findings persistence,
    and suggestion tracking.
    """

    SCHEMA_VERSION = 1

    CREATE_TABLES_SQL = """
    CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tool_name TEXT NOT NULL,
        tool_type TEXT NOT NULL,
        target TEXT NOT NULL,
        parameters TEXT,
        status TEXT NOT NULL DEFAULT 'running',
        exit_code INTEGER,
        raw_output TEXT,
        parsed_data TEXT,
        started_at TEXT NOT NULL,
        completed_at TEXT,
        duration_ms INTEGER DEFAULT 0,
        created_at TEXT NOT NULL DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS findings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scan_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        severity TEXT NOT NULL,
        category TEXT NOT NULL,
        details TEXT,
        explanation TEXT,
        created_at TEXT NOT NULL DEFAULT (datetime('now')),
        FOREIGN KEY (scan_id) REFERENCES scans(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS suggestions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scan_id INTEGER NOT NULL,
        recommended_tool TEXT NOT NULL,
        confidence REAL NOT NULL,
        confidence_label TEXT NOT NULL,
        reasoning TEXT,
        was_followed INTEGER DEFAULT 0,
        created_at TEXT NOT NULL DEFAULT (datetime('now')),
        FOREIGN KEY (scan_id) REFERENCES scans(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scan_id INTEGER NOT NULL,
        file_path TEXT NOT NULL,
        format TEXT NOT NULL DEFAULT 'html',
        generated_at TEXT NOT NULL DEFAULT (datetime('now')),
        FOREIGN KEY (scan_id) REFERENCES scans(id) ON DELETE CASCADE
    );
    """

    def __init__(self, db_path: str = ""):
        default_dir = os.path.expanduser("~/.kalinova")
        if not db_path:
            db_path = os.path.join(default_dir, "kalinova.db")

        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None
        self._init_db()

    def _init_db(self) -> None:
        """Initialize database and create tables."""
        try:
            self._conn = sqlite3.connect(self._db_path)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA foreign_keys = ON;")
            self._conn.executescript(self.CREATE_TABLES_SQL)
            self._conn.commit()
            logger.info(f"Database initialized: {self._db_path}")
        except sqlite3.Error as e:
            logger.error(f"Database initialization failed: {e}")
            raise

    def save_scan(
        self,
        tool_name: str,
        tool_type: str,
        target: str,
        parameters: dict,
        status: str,
        exit_code: int,
        raw_output: str,
        parsed_data: dict,
        started_at: datetime,
        completed_at: Optional[datetime] = None,
        duration_ms: int = 0,
    ) -> int:
        """
        Save a scan result to the database.

        Returns:
            Scan ID of the inserted record.
        """
        cursor = self._conn.execute(
            """
            INSERT INTO scans
                (tool_name, tool_type, target, parameters, status,
                 exit_code, raw_output, parsed_data, started_at,
                 completed_at, duration_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                tool_name, tool_type, target,
                json.dumps(parameters),
                status, exit_code, raw_output,
                json.dumps(parsed_data),
                started_at.isoformat(),
                completed_at.isoformat() if completed_at else None,
                duration_ms,
            ),
        )
        self._conn.commit()
        scan_id = cursor.lastrowid
        logger.info(f"Saved scan {scan_id}: {tool_name} → {target}")
        return scan_id

    def save_findings(self, scan_id: int, findings: list) -> None:
        """Save findings associated with a scan."""
        for f in findings:
            self._conn.execute(
                """
                INSERT INTO findings
                    (scan_id, description, severity, category, details, explanation)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    scan_id, f.description, f.severity,
                    f.category, json.dumps(f.details),
                    f.explanation,
                ),
            )
        self._conn.commit()
        logger.info(f"Saved {len(findings)} findings for scan {scan_id}")

    def save_suggestion(
        self, scan_id: int, recommended_tool: str,
        confidence: float, confidence_label: str,
        reasoning: str = "",
    ) -> int:
        """Save an ML suggestion."""
        cursor = self._conn.execute(
            """
            INSERT INTO suggestions
                (scan_id, recommended_tool, confidence, confidence_label, reasoning)
            VALUES (?, ?, ?, ?, ?)
            """,
            (scan_id, recommended_tool, confidence, confidence_label, reasoning),
        )
        self._conn.commit()
        return cursor.lastrowid

    def save_report(self, scan_id: int, file_path: str, fmt: str = "html") -> int:
        """Save report metadata."""
        cursor = self._conn.execute(
            "INSERT INTO reports (scan_id, file_path, format) VALUES (?, ?, ?)",
            (scan_id, file_path, fmt),
        )
        self._conn.commit()
        return cursor.lastrowid

    def get_scan_history(self, limit: int = 50) -> List[Dict]:
        """Get recent scan history."""
        cursor = self._conn.execute(
            "SELECT * FROM scans ORDER BY created_at DESC LIMIT ?",
            (limit,),
        )
        return [dict(row) for row in cursor.fetchall()]

    def get_scan(self, scan_id: int) -> Optional[Dict]:
        """Get a specific scan by ID."""
        cursor = self._conn.execute(
            "SELECT * FROM scans WHERE id = ?", (scan_id,),
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_findings_for_scan(self, scan_id: int) -> List[Dict]:
        """Get all findings for a scan."""
        cursor = self._conn.execute(
            "SELECT * FROM findings WHERE scan_id = ? ORDER BY severity",
            (scan_id,),
        )
        return [dict(row) for row in cursor.fetchall()]

    def get_suggestions_for_scan(self, scan_id: int) -> List[Dict]:
        """Get ML suggestions for a scan."""
        cursor = self._conn.execute(
            "SELECT * FROM suggestions WHERE scan_id = ?", (scan_id,),
        )
        return [dict(row) for row in cursor.fetchall()]

    def close(self) -> None:
        """Close the database connection."""
        if self._conn:
            self._conn.close()
            logger.info("Database connection closed.")
