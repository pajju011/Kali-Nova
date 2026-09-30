import os
import sys
import unittest
import sqlite3
import tempfile
from pathlib import Path

# Add kalinova root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.database import DatabaseManager
from config import (
    set_keyring_api_key,
    get_keyring_api_key,
    delete_keyring_api_key,
    resolve_api_key
)

class SecurityUpgradesTest(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_sec.db")
        os.environ["KALINOVA_DB_PATH"] = self.db_path
        DatabaseManager.initialize()

    def tearDown(self):
        self.temp_dir.cleanup()
        if "KALINOVA_DB_PATH" in os.environ:
            del os.environ["KALINOVA_DB_PATH"]

    def test_database_field_encryption_roundtrip(self):
        plain_secret = "Confidential vulnerability report: Port 445 SMBv1 exploitable"
        enc = DatabaseManager.encrypt_field(plain_secret)
        self.assertTrue(enc.startswith("ENC:v1:"))
        self.assertNotIn("SMBv1", enc)

        dec = DatabaseManager.decrypt_field(enc)
        self.assertEqual(dec, plain_secret)

    def test_database_backward_compatibility_with_plaintext(self):
        legacy_plaintext = "Legacy plaintext scan log without encryption"
        dec = DatabaseManager.decrypt_field(legacy_plaintext)
        self.assertEqual(dec, legacy_plaintext)

    def test_scans_stored_encrypted_at_rest(self):
        secret_stdout = "Sensitive findings: MySQL root password exposed: secret123"
        DatabaseManager.save_scan(
            target="192.168.1.50",
            tool_name="NMAP",
            command="nmap -sV 192.168.1.50",
            stdout=secret_stdout,
            parsed_ports="3306/tcp",
            risk_score=90,
            threat_level="CRITICAL"
        )

        # Verify raw SQLite content on disk is ciphertext
        raw_conn = sqlite3.connect(self.db_path)
        cursor = raw_conn.cursor()
        cursor.execute("SELECT stdout, command, parsed_ports FROM scans WHERE target = '192.168.1.50'")
        row = cursor.fetchone()
        raw_conn.close()

        self.assertIsNotNone(row)
        raw_stdout, raw_command, raw_ports = row
        self.assertTrue(raw_stdout.startswith("ENC:v1:"))
        self.assertNotIn("secret123", raw_stdout)

        # Verify DatabaseManager.get_all_scans() transparently decrypts
        scans = DatabaseManager.get_all_scans()
        self.assertGreater(len(scans), 0)
        latest = scans[0]
        self.assertEqual(latest["stdout"], secret_stdout)
        self.assertEqual(latest["command"], "nmap -sV 192.168.1.50")
        self.assertEqual(latest["parsed_ports"], "3306/tcp")

    def test_chat_history_encrypted_at_rest(self):
        chat_prompt = "User prompt containing sensitive internal domain: internal.corp.net"
        DatabaseManager.save_chat_message("user", chat_prompt)

        raw_conn = sqlite3.connect(self.db_path)
        cursor = raw_conn.cursor()
        cursor.execute("SELECT message FROM ai_chat_history LIMIT 1")
        row = cursor.fetchone()
        raw_conn.close()

        self.assertIsNotNone(row)
        self.assertTrue(row[0].startswith("ENC:v1:"))
        self.assertNotIn("internal.corp.net", row[0])

        history = DatabaseManager.get_chat_history()
        self.assertEqual(history[0]["message"], chat_prompt)

    def test_keyring_and_secure_keystore_integration(self):
        provider = "test_ai_provider"
        secret_key = "sk-live-test-secret-key-998877"

        # Save key
        saved = set_keyring_api_key(provider, secret_key)
        self.assertTrue(saved)

        # Retrieve key
        fetched = get_keyring_api_key(provider)
        self.assertEqual(fetched, secret_key)

        # Resolve key
        resolved = resolve_api_key(provider)
        self.assertEqual(resolved, secret_key)

        # Delete key
        deleted = delete_keyring_api_key(provider)
        self.assertTrue(deleted)
        self.assertEqual(get_keyring_api_key(provider), "")


if __name__ == "__main__":
    unittest.main()
