import unittest
import os
import sys
import tempfile

# Ensure kalinova is in Python path for test execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import load_config, save_config, resolve_api_key
from core.database import DatabaseManager
from core.ai_copilot import AICopilot

class TestAIIntegration(unittest.TestCase):

    def setUp(self):
        self.old_db_path = os.environ.get("KALINOVA_DB_PATH")
        self.temp_dir = tempfile.TemporaryDirectory()
        os.environ["KALINOVA_DB_PATH"] = os.path.join(self.temp_dir.name, "test_kalinova.db")
        DatabaseManager.initialize()

    def tearDown(self):
        self.temp_dir.cleanup()
        if self.old_db_path is not None:
            os.environ["KALINOVA_DB_PATH"] = self.old_db_path
        else:
            os.environ.pop("KALINOVA_DB_PATH", None)

    def test_user_isolated_db_path(self):
        db_path = DatabaseManager.get_db_path()
        self.assertTrue(db_path.endswith("test_kalinova.db"))

    def test_config_save_and_load(self):
        test_data = {
            "ai_provider": "gemini",
            "api_key": "TEST_KEY_12345",
            "model": "gemini-2.0-flash",
            "ollama_url": "http://localhost:11434",
            "app_mode": "Professional"
        }
        saved = save_config(test_data)
        self.assertTrue(saved)

        loaded = load_config()
        self.assertEqual(loaded["ai_provider"], "gemini")
        self.assertEqual(loaded["api_key"], "TEST_KEY_12345")
        self.assertEqual(loaded["model"], "gemini-2.0-flash")

    def test_environment_api_key_resolution(self):
        os.environ["GEMINI_API_KEY"] = "ENV_GEMINI_KEY_999"
        key = resolve_api_key("gemini", explicit_key="")
        self.assertEqual(key, "ENV_GEMINI_KEY_999")
        os.environ.pop("GEMINI_API_KEY", None)

    def test_ai_copilot_heuristic_fallback(self):
        save_config({"ai_provider": "heuristic", "api_key": "", "model": ""})
        response = AICopilot.query_llm(context_info="Target 127.0.0.1", user_prompt="How do I use Nmap?")
        self.assertIn("AI Copilot Helper", response)
        self.assertIn("Nmap", response)

    def test_ai_copilot_tool_specific_queries(self):
        save_config({"ai_provider": "heuristic", "api_key": "", "model": ""})
        
        nikto_resp = AICopilot.query_llm(context_info="Active Tool: Nikto", user_prompt="What does Nikto do?")
        self.assertIn("Nikto Web Scanner", nikto_resp)

        sqlmap_resp = AICopilot.query_llm(context_info="Active Tool: SQLmap", user_prompt="How to patch SQLi?")
        self.assertIn("SQLmap", sqlmap_resp)
        self.assertIn("Security Recommendation", sqlmap_resp)

    def test_ai_copilot_expanded_vulnerability_topics(self):
        save_config({"ai_provider": "heuristic", "api_key": "", "model": ""})
        
        xss_resp = AICopilot.query_llm(context_info="", user_prompt="How to patch XSS vulnerability?")
        self.assertIn("Cross-Site Scripting", xss_resp)
        self.assertIn("html.escape", xss_resp)

        rce_resp = AICopilot.query_llm(context_info="", user_prompt="Explain RCE command injection remediation")
        self.assertIn("Remote Code Execution", rce_resp)
        self.assertIn("subprocess.run", rce_resp)

        priv_resp = AICopilot.query_llm(context_info="", user_prompt="How to check for Linux privilege escalation?")
        self.assertIn("Privilege Escalation", priv_resp)
        self.assertIn("sudo -l", priv_resp)

    def test_ai_copilot_missing_gemini_key_resilient_fallback(self):
        save_config({"ai_provider": "gemini", "api_key": "", "model": "gemini-2.0-flash"})
        response = AICopilot.query_llm(context_info="Nmap scan logs", user_prompt="Explain vulnerability")
        self.assertIn("API key is missing", response)
        self.assertIn("OFFLINE SECURITY ADVISORY FALLBACK", response)

    def test_chat_history_persistence(self):
        DatabaseManager.clear_chat_history()
        DatabaseManager.save_chat_message("user", "Hello AI Copilot")
        DatabaseManager.save_chat_message("assistant", "Hello Security Analyst")

        history = DatabaseManager.get_chat_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["role"], "user")
        self.assertEqual(history[0]["message"], "Hello AI Copilot")
        self.assertEqual(history[1]["role"], "assistant")
        self.assertEqual(history[1]["message"], "Hello Security Analyst")


