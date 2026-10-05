import unittest
import os
import sys

# Ensure kalinova is in Python path for test execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.database import DatabaseManager
from core.ai_copilot import AICopilot

class TestProfessionalSuite(unittest.TestCase):

    def setUp(self):
        # Use a temporary database for test runs if preferred,
        # but let's just make sure tests use the standard setup
        # and clean up their modifications.
        DatabaseManager.initialize()

    def tearDown(self):
        # We can keep database clean
        pass

    def test_database_persistence(self):
        # 1. Insert a scan
        DatabaseManager.save_scan(
            target="test-target.local",
            tool_name="NMAP",
            command="nmap -p 22,80 test-target.local",
            stdout="Starting scan...\nPort 22 is open\nPort 80 is open",
            parsed_ports="22,80",
            risk_score=45,
            threat_level="MEDIUM"
        )

        # 2. Query scans
        scans = DatabaseManager.get_all_scans()
        self.assertGreater(len(scans), 0)

        # Verify details of latest scan
        latest = scans[0]
        self.assertEqual(latest["target"], "test-target.local")
        self.assertEqual(latest["tool_name"], "NMAP")
        self.assertEqual(latest["parsed_ports"], "22,80")
        self.assertEqual(latest["risk_score"], 45)
        self.assertEqual(latest["threat_level"], "MEDIUM")

        # 3. Delete the scan
        DatabaseManager.delete_scan(latest["id"])
        scans_after = DatabaseManager.get_all_scans()
        # Verify the scan was removed (or count went down)
        self.assertEqual(len(scans_after), len(scans) - 1)

    def test_copilot_diagnose_vulnerabilities(self):
        # Test event-based diagnostics
        findings = AICopilot.diagnose(events=["SQL_INJECTION"], open_ports=[])
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["title"], "SQL Injection Vulnerability")
        self.assertEqual(findings[0]["severity"], "CRITICAL")
        self.assertIn("Python Parameterized Query", findings[0]["remediation_python"])

    def test_copilot_diagnose_ports(self):
        # Test port-based diagnostics
        findings = AICopilot.diagnose(events=[], open_ports=[22, 3306])
        self.assertEqual(len(findings), 2)
        
        titles = [f["title"] for f in findings]
        self.assertIn("SSH Service Public Access", titles)
        self.assertIn("Database Instance Port Publicly Exposed", titles)

    def test_copilot_diagnose_empty(self):
        # Test empty diagnostics fallback
        findings = AICopilot.diagnose(events=[], open_ports=[])
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["title"], "Standard Host Hardening Recommendations")
        self.assertEqual(findings[0]["severity"], "LOW")
