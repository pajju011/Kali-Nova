import json
import urllib.request
import urllib.error
from PyQt6.QtCore import QThread, pyqtSignal
from config import load_config
from core.database import DatabaseManager

class AICopilot:

    SYSTEM_PROMPT = (
        "You are Kali-Nova AI Copilot, a highly skilled ethical hacking advisor and penetration testing copilot on Kali Linux.\n"
        "Your task is to analyze security tool execution outputs (such as Nmap, Nikto, Sqlmap, Whois, etc.), identify open ports and vulnerabilities, assess CVSS threat severity, and deliver actionable remediation code patches in Python, Node.js, or Bash.\n"
        "Keep responses professional, structured, concise, and focused on defensive remediation and authorization boundary compliance."
    )

    VULN_MAPPINGS = {
        "SQL_INJECTION": {
            "title": "SQL Injection Vulnerability",
            "cvss": 9.8,
            "severity": "CRITICAL",
            "description": "Untrusted input was directly concatenated into a database SQL query, enabling unauthorized remote code execution, database leakage, or data tampering.",
            "remediation_python": """# [REMEDIATION] Python Parameterized Query
import sqlite3

def secure_query(user_input):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    # SECURE: Always use placeholders (?) instead of string interpolation
    cursor.execute("SELECT * FROM users WHERE username = ?", (user_input,))
    return cursor.fetchall()
""",
            "remediation_node": """// [REMEDIATION] Node.js Safe SQL Statement
const { Client } = require('pg');

async function secureQuery(userInput) {
    const client = new Client();
    await client.connect();
    // SECURE: Use parameterized query object
    const query = {
        text: 'SELECT * FROM users WHERE username = $1',
        values: [userInput],
    };
    const res = await client.query(query);
    return res.rows;
}
"""
        },
        "BRUTE_FORCE": {
            "title": "Weak Authentication Lockout Control",
            "cvss": 7.5,
            "severity": "HIGH",
            "description": "No rate limiting or request throttling detected on SSH/HTTP portals, making the application highly susceptible to brute-force credential stuffing.",
            "remediation_python": """# [REMEDIATION] Implement Fail2ban Jails for SSH
# Add the following to /etc/fail2ban/jail.local:

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
""",
            "remediation_node": """// [REMEDIATION] Node.js Rate Limiting Middleware
const rateLimit = require('express-rate-limit');

const loginLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 5, // Limit each IP to 5 requests per windowMs
    message: 'Too many authentication attempts. Please try again later.'
});

module.exports = loginLimiter;
"""
        },
        "DIR_ENUM": {
            "title": "Information Disclosure via Directory Indexing",
            "cvss": 5.3,
            "severity": "MEDIUM",
            "description": "Sensitive application pathways, backup zip archives, or developer environment configs were discovered via directory brute forcing.",
            "remediation_python": """# [REMEDIATION] Nginx Server Token & Directory Options
server {
    listen 80;
    server_name example.com;

    location / {
        # SECURE: Disable directory autoindexing to prevent directory listing
        autoindex off;
    }
}
""",
            "remediation_node": """// [REMEDIATION] Node.js Helmet Security Headers
const express = require('express');
const helmet = require('helmet');
const app = express();

// SECURE: Mount Helmet to hide x-powered-by header and apply security controls
app.use(helmet());
"""
        },
        "EMAIL_ENUM": {
            "title": "OSINT Personal Identifiable Information Leakage",
            "cvss": 4.0,
            "severity": "LOW",
            "description": "Corporate email addresses or personal identifiers were collected passively from open-source metadata, fueling potential spear-phishing entry vectors.",
            "remediation_python": """# [REMEDIATION] Metadata Scrubbing Script
import subprocess

def strip_image_metadata(image_path):
    # SECURE: ExifTool can be run to scrub GPS/Authors metadata from file uploads
    subprocess.run(["exiftool", "-all=", "-overwrite_original", image_path])
""",
            "remediation_node": """// [REMEDIATION] HTML Obfuscation Pattern
// To protect corporate emails from automated scrapers:
// Write emails dynamically via JavaScript instead of plain text tags:
const secureEmail = 'info' + '@' + 'targetdomain.com';
"""
        }
    }

    PORT_MAPPINGS = {
        21: {
            "title": "FTP Service Exposed (Insecure Protocol)",
            "cvss": 7.4,
            "severity": "HIGH",
            "description": "Port 21 FTP transmits credentials and transaction data in clear text, exposing communications to passive sniffing attacks.",
            "remediation": "Transition from insecure legacy FTP protocols to secure SFTP (SSH File Transfer Protocol) or FTPS (FTP over SSL/TLS)."
        },
        22: {
            "title": "SSH Service Public Access",
            "cvss": 5.3,
            "severity": "MEDIUM",
            "description": "SSH access is listening publicly on default Port 22, facilitating constant brute force logins.",
            "remediation": "Restrict SSH access behind a secure VPN or IP whitelist. Enforce key-based authentication (`PasswordAuthentication no`) in /etc/ssh/sshd_config."
        },
        80: {
            "title": "Cleartext HTTP Service Allowed",
            "cvss": 4.8,
            "severity": "MEDIUM",
            "description": "Web server accepts unencrypted HTTP connections. Session tokens and user inputs are subject to man-in-the-middle decryption.",
            "remediation": "Redirect all cleartext port 80 traffic to encrypted SSL/TLS port 443 with HSTS headers enabled."
        },
        443: {
            "title": "SSL/TLS Port (General Hardening)",
            "cvss": 2.5,
            "severity": "LOW",
            "description": "Standard HTTPS server is active. Ensure modern cipher suites and protocol versions (TLS 1.2/1.3) are locked in.",
            "remediation": "Disable old SSL v3, TLS 1.0, and TLS 1.1 protocols. Utilize robust ECDHE/DHE key exchange mechanisms."
        },
        3306: {
            "title": "Database Instance Port Publicly Exposed",
            "cvss": 8.8,
            "severity": "HIGH",
            "description": "MySQL database instance Port 3306 is exposed. Direct database connection brute forcing is possible.",
            "remediation": "Bind the database connection listener to localhost (`bind-address = 127.0.0.1` in my.cnf) and wrap database relays in encrypted SSH tunnels."
        },
        8080: {
            "title": "Standard Alternative HTTP/S Port Active",
            "cvss": 5.3,
            "severity": "MEDIUM",
            "description": "Port 8080 web services are often dev servers, missing strict production headers or enterprise access controls.",
            "remediation": "Verify all proxy/gateway configurations match production security protocols, hiding alternate ports behind an API Gateway."
        }
    }

    @staticmethod
    def diagnose(events, open_ports):
        """Rule-based heuristic diagnostic method preserved for backward compatibility and offline mode."""
        findings = []

        # 1. Process Events
        for ev in events:
            if ev in AICopilot.VULN_MAPPINGS:
                findings.append(AICopilot.VULN_MAPPINGS[ev])

        # 2. Process Ports
        for port in open_ports:
            if port in AICopilot.PORT_MAPPINGS:
                pm = AICopilot.PORT_MAPPINGS[port]
                findings.append({
                    "title": pm["title"],
                    "cvss": pm["cvss"],
                    "severity": pm["severity"],
                    "description": pm["description"],
                    "remediation_python": f"# [REMEDIATION] {pm['title']}\n# Security Directive:\n# {pm['remediation']}\n",
                    "remediation_node": f"// [REMEDIATION] {pm['title']}\n// Security Directive:\n// {pm['remediation']}\n"
                })

        # Return default findings if empty
        if not findings:
            findings.append({
                "title": "Standard Host Hardening Recommendations",
                "cvss": 2.5,
                "severity": "LOW",
                "description": "No immediate high-severity socket vulnerabilities or event anomalies were observed. Run comprehensive Nmap or web directory vulnerability sweeps.",
                "remediation_python": "# [REMEDIATION] General Host Patching\n# Establish fail2ban rules and update system packages regularly.\n",
                "remediation_node": "// [REMEDIATION] General Host Patching\n// Establish system-wide service token updates regularly.\n"
            })

        return findings

    @staticmethod
    def query_llm(context_info: str = "", user_prompt: str = "") -> str:
        """Main AI query router. Selects provider based on user config."""
        config = load_config()
        provider = config.get("ai_provider", "heuristic").lower()
        api_key = config.get("api_key", "").strip()
        model = config.get("model", "gemini-1.5-flash").strip()
        ollama_url = config.get("ollama_url", "http://localhost:11434").strip()

        if provider == "gemini":
            if not api_key:
                return "⚠️ [Google Gemini Error] API key is missing. Please go to Settings and enter your Gemini API key."
            return AICopilot._query_gemini(context_info, user_prompt, api_key, model)

        elif provider == "openai":
            if not api_key:
                return "⚠️ [OpenAI Error] API key is missing. Please go to Settings and enter your OpenAI API key."
            return AICopilot._query_openai(context_info, user_prompt, api_key, model)

        elif provider == "ollama":
            return AICopilot._query_ollama(context_info, user_prompt, model, ollama_url)

        else:
            # Heuristic offline fallback
            heuristic_findings = AICopilot.diagnose(events=[], open_ports=[])
            resp = "🔍 **[Offline Rule Diagnostics]**\n\n"
            for f in heuristic_findings:
                resp += f"• **{f['title']}** (Severity: {f['severity']})\n  {f['description']}\n\n"
            resp += "*To enable live LLM intelligence, select Google Gemini, OpenAI, or Ollama in Kali-Nova Settings.*"
            return resp

    @staticmethod
    def _query_gemini(context_info: str, user_prompt: str, api_key: str, model: str) -> str:
        model_name = model if model else "gemini-1.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        
        full_text = f"{AICopilot.SYSTEM_PROMPT}\n\n--- SECURITY SCAN CONTEXT ---\n{context_info}\n\n--- USER QUESTION ---\n{user_prompt}"
        
        payload = {
            "contents": [
                {
                    "parts": [{"text": full_text}]
                }
            ]
        }

        try:
            req_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=req_data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode("utf-8"))
                candidates = result.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "No content returned.")
                return "⚠️ [Gemini] Received empty response from Google Gemini API."
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            return f"❌ [Gemini HTTP Error {e.code}]: {err_body}"
        except Exception as e:
            return f"❌ [Gemini Connection Error]: {str(e)}"

    @staticmethod
    def _query_openai(context_info: str, user_prompt: str, api_key: str, model: str) -> str:
        model_name = model if model else "gpt-4o-mini"
        url = "https://api.openai.com/v1/chat/completions"

        messages = [
            {"role": "system", "content": AICopilot.SYSTEM_PROMPT},
            {"role": "user", "content": f"Security Scan Context:\n{context_info}\n\nUser Question:\n{user_prompt}"}
        ]

        payload = {
            "model": model_name,
            "messages": messages,
            "temperature": 0.3
        }

        try:
            req_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=req_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode("utf-8"))
                choices = result.get("choices", [])
                if choices:
                    return choices[0].get("message", {}).get("content", "No content returned.")
                return "⚠️ [OpenAI] Received empty response from OpenAI API."
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            return f"❌ [OpenAI HTTP Error {e.code}]: {err_body}"
        except Exception as e:
            return f"❌ [OpenAI Connection Error]: {str(e)}"

    @staticmethod
    def _query_ollama(context_info: str, user_prompt: str, model: str, ollama_url: str) -> str:
        model_name = model if model else "llama3:8b"
        endpoint = f"{ollama_url.rstrip('/')}/api/generate"

        prompt = f"{AICopilot.SYSTEM_PROMPT}\n\n--- SECURITY SCAN CONTEXT ---\n{context_info}\n\n--- USER QUESTION ---\n{user_prompt}"
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }

        try:
            req_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                endpoint,
                data=req_data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=45) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result.get("response", "No response generated by Ollama.")
        except Exception as e:
            return f"❌ [Ollama Offline Error]: Cannot connect to Ollama at `{ollama_url}`.\nMake sure Ollama is installed and running (`ollama serve`). Details: {str(e)}"


class AIWorkerThread(QThread):
    """Asynchronous worker thread to execute LLM API queries without locking the PyQt6 GUI loop."""
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, context_info: str = "", user_prompt: str = ""):
        super().__init__()
        self.context_info = context_info
        self.user_prompt = user_prompt

    def run(self):
        try:
            response = AICopilot.query_llm(self.context_info, self.user_prompt)
            # Save message to database chat history
            if self.user_prompt:
                DatabaseManager.save_chat_message("user", self.user_prompt)
            DatabaseManager.save_chat_message("assistant", response)
            self.finished_signal.emit(response)
        except Exception as e:
            self.error_signal.emit(f"Worker Error: {str(e)}")
