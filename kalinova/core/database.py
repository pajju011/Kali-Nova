import base64
import hashlib
import hmac
import os
import sqlite3
from pathlib import Path
from datetime import datetime

class DatabaseManager:
    DB_FILE = "kalinova.db"

    @staticmethod
    def _derive_db_key() -> bytes:
        """Derives a machine-isolated master encryption key for local SQLite data encryption."""
        machine_seed = os.environ.get("COMPUTERNAME", "") + os.environ.get("USERNAME", "") + os.environ.get("USER", "")
        salt = b"kalinova_secure_sqlite_storage_v1"
        return hashlib.sha256(machine_seed.encode("utf-8") + salt).digest()

    @staticmethod
    def encrypt_field(text: str) -> str:
        """Encrypts sensitive database field using authenticated CTR-keystream with HMAC-SHA256."""
        if not text:
            return ""
        key = DatabaseManager._derive_db_key()
        iv = os.urandom(16)
        data = text.encode("utf-8")
        keystream = bytearray()
        counter = 0
        while len(keystream) < len(data):
            block = hmac.new(key, iv + counter.to_bytes(4, "big"), hashlib.sha256).digest()
            keystream.extend(block)
            counter += 1
        cipher = bytes(d ^ k for d, k in zip(data, keystream[:len(data)]))
        tag = hmac.new(key, iv + cipher, hashlib.sha256).digest()[:16]
        return "ENC:v1:" + base64.b64encode(iv + tag + cipher).decode("utf-8")

    @staticmethod
    def decrypt_field(enc_text: str) -> str:
        """Decrypts database field with automatic backward-compatibility fallback for plaintext records."""
        if not enc_text or not enc_text.startswith("ENC:v1:"):
            return enc_text
        try:
            key = DatabaseManager._derive_db_key()
            raw = base64.b64decode(enc_text[7:])
            if len(raw) < 32:
                return enc_text
            iv, tag, cipher = raw[:16], raw[16:32], raw[32:]
            expected_tag = hmac.new(key, iv + cipher, hashlib.sha256).digest()[:16]
            if not hmac.compare_digest(tag, expected_tag):
                return enc_text
            keystream = bytearray()
            counter = 0
            while len(keystream) < len(cipher):
                block = hmac.new(key, iv + counter.to_bytes(4, "big"), hashlib.sha256).digest()
                keystream.extend(block)
                counter += 1
            plain = bytes(c ^ k for c, k in zip(cipher, keystream[:len(cipher)]))
            return plain.decode("utf-8", errors="replace")
        except Exception:
            return enc_text

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
        conn = sqlite3.connect(DatabaseManager.get_db_path())
        try:
            # Enable SQLCipher PRAGMA encryption key if SQLCipher library is loaded
            key_hex = DatabaseManager._derive_db_key().hex()
            conn.execute(f"PRAGMA key = \"x'{key_hex}'\"")
        except Exception:
            pass
        return conn

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
        enc_command = DatabaseManager.encrypt_field(command or "")
        enc_stdout = DatabaseManager.encrypt_field(stdout or "")
        enc_ports = DatabaseManager.encrypt_field(parsed_ports or "")
        cursor.execute("""
            INSERT INTO scans (target, tool_name, command, stdout, parsed_ports, risk_score, threat_level, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (target, tool_name, enc_command, enc_stdout, enc_ports, risk_score, threat_level, timestamp))
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
                "command": DatabaseManager.decrypt_field(row[3]),
                "stdout": DatabaseManager.decrypt_field(row[4]),
                "parsed_ports": DatabaseManager.decrypt_field(row[5]),
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
        enc_msg = DatabaseManager.encrypt_field(message or "")
        cursor.execute("""
            INSERT INTO ai_chat_history (role, message, timestamp)
            VALUES (?, ?, ?)
        """, (role, enc_msg, timestamp))
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
                "message": DatabaseManager.decrypt_field(row[2]),
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
