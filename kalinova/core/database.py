import sqlite3
import os
from pathlib import Path
from datetime import datetime

class DatabaseManager:
    DB_FILE = "kalinova.db"

    @staticmethod
    def get_db_path() -> str:
        """Returns user-isolated database file path or environment override if set."""
        env_path = os.environ.get("KALINOVA_DB_PATH")
        if env_path:
            return env_path
        
        if os.name == 'nt':
            base_dir = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        else:
            base_dir = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
        
        data_dir = base_dir / "kalinova"
        data_dir.mkdir(parents=True, exist_ok=True)
        return str(data_dir / DatabaseManager.DB_FILE)

    @staticmethod
    def get_connection():
        return sqlite3.connect(DatabaseManager.get_db_path())

    @staticmethod
    def initialize():
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL,
                tool_name TEXT NOT NULL,
                command TEXT NOT NULL,
                stdout TEXT NOT NULL,
                parsed_ports TEXT NOT NULL,
                risk_score INTEGER NOT NULL,
                threat_level TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def save_scan(target, tool_name, command, stdout, parsed_ports, risk_score, threat_level):
        DatabaseManager.initialize()
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO scans (target, tool_name, command, stdout, parsed_ports, risk_score, threat_level, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (target, tool_name, command, stdout, parsed_ports, risk_score, threat_level, timestamp))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_scans():
        DatabaseManager.initialize()
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, target, tool_name, command, stdout, parsed_ports, risk_score, threat_level, timestamp FROM scans ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()

        scans = []
        for row in rows:
            scans.append({
                "id": row[0],
                "target": row[1],
                "tool_name": row[2],
                "command": row[3],
                "stdout": row[4],
                "parsed_ports": row[5],
                "risk_score": row[6],
                "threat_level": row[7],
                "timestamp": row[8]
            })
        return scans

    @staticmethod
    def delete_scan(scan_id):
        DatabaseManager.initialize()
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM scans WHERE id = ?", (scan_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def save_chat_message(role: str, message: str):
        DatabaseManager.initialize()
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO ai_chat_history (role, message, timestamp)
            VALUES (?, ?, ?)
        """, (role, message, timestamp))
        conn.commit()
        conn.close()

    @staticmethod
    def get_chat_history(limit: int = 50):
        DatabaseManager.initialize()
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, role, message, timestamp FROM ai_chat_history ORDER BY id ASC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()

        history = []
        for row in rows:
            history.append({
                "id": row[0],
                "role": row[1],
                "message": row[2],
                "timestamp": row[3]
            })
        return history

    @staticmethod
    def clear_chat_history():
        DatabaseManager.initialize()
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ai_chat_history")
        conn.commit()
        conn.close()

# Initialize immediately on import
DatabaseManager.initialize()
