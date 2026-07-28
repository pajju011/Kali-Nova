import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    DB_FILE = "kalinova.db"

    @staticmethod
    def get_connection():
        return sqlite3.connect(DatabaseManager.DB_FILE)

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

# Initialize immediately on import
DatabaseManager.initialize()
