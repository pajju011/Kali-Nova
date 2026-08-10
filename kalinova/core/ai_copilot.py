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
            return AICopilot._query_heuristic(context_info, user_prompt)

    @staticmethod
    def _query_heuristic(context_info: str = "", user_prompt: str = "") -> str:
        prompt_lower = user_prompt.lower().strip()
        context_lower = context_info.lower().strip()

        tools_db = {
            "nmap": {
                "name": "Nmap (Network Mapper)",
                "usage": "nmap -sV -A <target_ip>",
                "description": "Nmap is an open-source network discovery and vulnerability scanner used to discover hosts, open ports, and running service versions.",
                "flags": [
                    "• `-sV`: Enable service/version detection on open ports.",
                    "• `-A`: Aggressive scan mode (enables OS detection, version detection, script scanning, and traceroute).",
                    "• `-p <ports>`: Specify custom target port numbers (e.g. `-p 80,443` or `-p 1-65535`).",
                    "• `-sS`: Stealth SYN scan (requires root/sudo privileges)."
                ],
                "advice": "Run service detection `-sV` first to identify exposed services, then analyze specific open ports for outdated software versions."
            },
            "nikto": {
                "name": "Nikto Web Scanner",
                "usage": "nikto -h http://<target_url>",
                "description": "Nikto performs comprehensive web server testing for dangerous files, outdated server software, and misconfigured headers.",
                "flags": [
                    "• `-h <host>`: Target host URL or IP address.",
                    "• `-ssl`: Force SSL/TLS encrypted connection mode.",
                    "• `-Call`: Test all CGI directories."
                ],
                "advice": "Use Nikto to audit web server headers (X-Frame-Options, CSP, HSTS) and hidden administrative directories."
            },
            "sqlmap": {
                "name": "SQLmap Automatic SQL Injection Engine",
                "usage": "sqlmap -u \"http://target.com/page.php?id=1\" --batch",
                "description": "SQLmap detects and exploits SQL injection vulnerabilities in web application database parameters.",
                "flags": [
                    "• `-u <url>`: Target URL containing dynamic GET/POST parameters.",
                    "• `--batch`: Run non-interactively with default answers.",
                    "• `--level=1..5`: Increase test depth (Level 5 tests HTTP headers like Referer and User-Agent).",
                    "• `--dbs`: Enumerate available database names upon successful injection."
                ],
                "advice": "Remediate SQL injection by converting raw SQL queries to parameterized queries (Prepared Statements)."
            },
            "gobuster": {
                "name": "Gobuster Directory Brute Force",
                "usage": "gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/common.txt",
                "description": "Gobuster performs high-speed directory and file brute-forcing on web servers to locate hidden URIs.",
                "flags": [
                    "• `dir`: Directory brute-forcing mode.",
                    "• `-u <url>`: Target URL.",
                    "• `-w <wordlist>`: Path to wordlist dictionary.",
                    "• `-x php,txt,html`: Search for specific file extensions."
                ],
                "advice": "Disable directory autoindexing (`autoindex off;`) and restrict access to backup zip files or `.env` configs."
            },
            "wfuzz": {
                "name": "Wfuzz Web Application Fuzzer",
                "usage": "wfuzz -c -z file,wordlist.txt --hc 404 http://example.com/FUZZ",
                "description": "Wfuzz is a flexible web fuzzer designed to test parameters, directories, and headers by replacing `FUZZ` placeholders.",
                "flags": [
                    "• `-z file,<path>`: Specify wordlist payload generator.",
                    "• `--hc 404`: Hide response HTTP status code 404.",
                    "• `-c`: Enable colorized output format."
                ],
                "advice": "Filter out common error HTTP status codes (`--hc 404,403`) to highlight valid endpoints."
            },
            "hydra": {
                "name": "Hydra Network Login Cracker",
                "usage": "hydra -l admin -P passwords.txt <target_ip> ssh",
                "description": "Hydra is a parallelized login brute-forcer supporting SSH, FTP, HTTP-Form, SMB, MySQL, and database services.",
                "flags": [
                    "• `-l <user>` / `-L <userlist>`: Target username or user list file.",
                    "• `-p <pass>` / `-P <passlist>`: Password or dictionary list file.",
                    "• `<service>`: Protocol target (ssh, ftp, http-post-form, etc.)."
                ],
                "advice": "Mitigate Hydra brute forcing by enforcing Fail2ban rate-limiting and SSH key-based authentication."
            },
            "john": {
                "name": "John the Ripper Password Cracker",
                "usage": "john --wordlist=passwords.txt hash_file.txt",
                "description": "John the Ripper cracks password hashes using dictionary, rule-based, and brute-force modes.",
                "flags": [
                    "• `--wordlist=<path>`: Wordlist path for dictionary attack.",
                    "• `--format=<format>`: Explicitly define hash format (e.g. `raw-md5`, `NT`, `sha512crypt`).",
                    "• `--show`: Display previously cracked password entries."
                ],
                "advice": "Migrate legacy hash algorithms (MD5, SHA1) to key-stretching hashing functions like bcrypt or Argon2id."
            },
            "hashid": {
                "name": "HashID & Hash Identifier",
                "usage": "hashid <hash_string>",
                "description": "Identifies password hash types based on length, character set, and structural signatures.",
                "flags": [
                    "• `-m`: Show corresponding Hashcat mode IDs.",
                    "• `-j`: Show corresponding John the Ripper format strings."
                ],
                "advice": "Use HashID to determine proper formatting before invoking John the Ripper or Hashcat."
            },
            "netcat": {
                "name": "Netcat (nc) Swiss Army Knife",
                "usage": "nc -lvnp 4444 (Listener) | nc <ip> <port> (Client)",
                "description": "Netcat reads and writes data across network connections using TCP/UDP protocols.",
                "flags": [
                    "• `-l`: Listen mode for incoming connections.",
                    "• `-v`: Verbose output mode.",
                    "• `-n`: Skip DNS resolution.",
                    "• `-p`: Specify local listener port number."
                ],
                "advice": "Ensure exposed listening ports are protected with firewall rules and encrypted payloads."
            },
            "wireshark": {
                "name": "Wireshark Packet Analyzer",
                "usage": "wireshark",
                "description": "Wireshark provides deep packet inspection and live traffic capture across network interfaces.",
                "flags": [
                    "• Capture Filters: `host 192.168.1.1` or `port 80`",
                    "• Display Filters: `http.request.method == \"POST\"` or `tcp.flags.syn == 1`"
                ],
                "advice": "Enforce HTTPS/TLS to prevent sensitive plaintext data leakage on packet analyzers."
            },
            "wifite": {
                "name": "Wifite 2 Wireless Security Auditor",
                "usage": "wifite -i wlan0mon --wpa",
                "description": "Wifite automates wireless network auditing for WEP, WPA/WPA2 handshakes, WPS PINs, and PMKID capture.",
                "flags": [
                    "• `-i <interface>`: Specify wireless monitor-mode interface.",
                    "• `--wpa`: Target WPA/WPA2 networks only.",
                    "• `--kill`: Terminate conflicting background processes."
                ],
                "advice": "Disable WPS on wireless routers and use strong WPA3-SAE passphrases."
            },
            "autopsy": {
                "name": "Autopsy Digital Forensics Browser",
                "usage": "autopsy -d /var/lib/autopsy -p 9999",
                "description": "Autopsy provides a web-based GUI for forensic disk analysis, evidence analysis, and deleted file recovery.",
                "flags": [
                    "• `-d <dir>`: Base directory for evidence storage.",
                    "• `-p <port>`: Port number for HTML browser interface."
                ],
                "advice": "Use read-only forensic write-blockers when attaching target drive media."
            },
            "sslscan": {
                "name": "SSLScan SSL/TLS Protocol Auditor",
                "usage": "sslscan <target_host>:443",
                "description": "SSLScan audits SSL/TLS services for supported ciphers, preferred protocols, and TLS vulnerabilities.",
                "flags": [
                    "• `--no-failed`: Hide unsupported cipher suites.",
                    "• `--show-certificate`: Display full X.509 certificate metadata."
                ],
                "advice": "Disable SSLv3, TLS 1.0, and TLS 1.1; enforce TLS 1.2+ with modern ECDHE cipher suites."
            },
            "sslyze": {
                "name": "SSLyze Python SSL Analyzer",
                "usage": "sslyze <target_host>",
                "description": "SSLyze analyzes SSL/TLS configurations, certificate validation, robot attacks, and session renegotiation.",
                "flags": ["• `--regular`: Perform standard suite of SSL/TLS security checks."],
                "advice": "Verify certificate chain trust and deploy HTTP Strict Transport Security (HSTS)."
            },
            "tlssled": {
                "name": "TLSSLed Shell Wrapper",
                "usage": "tlssled <host> <port>",
                "description": "TLSSLed evaluates SSL/TLS web servers based on sslscan and openssl checks.",
                "flags": ["• `<host> <port>`: Specify host address and target SSL port."],
                "advice": "Review output for weak 56-bit or 40-bit export ciphers."
            },
            "whois": {
                "name": "Whois Domain Lookup",
                "usage": "whois <domain.com>",
                "description": "Whois queries domain name registrar records, owner contact details, and DNS name servers.",
                "flags": ["• `<domain>`: Target domain name."],
                "advice": "Enable WHOIS privacy protection to hide owner email addresses from scrapers."
            },
            "harvester": {
                "name": "theHarvester OSINT Collector",
                "usage": "theHarvester -d <domain> -b google",
                "description": "theHarvester gathers emails, subdomains, hosts, employee names, and open ports from public search engines.",
                "flags": [
                    "• `-d <domain>`: Target company domain.",
                    "• `-b <source>`: Data source (google, bing, duckduckgo, etc.)."
                ],
                "advice": "Train employees to spot spear-phishing attempts leveraging OSINT email leakage."
            }
        }

        matched_tool_key = None
        for key in tools_db:
            if key in prompt_lower or key in context_lower:
                matched_tool_key = key
                break

        form_inputs_text = ""
        if "User Form Inputs:" in context_info:
            parts = context_info.split("User Form Inputs:")
            if len(parts) > 1:
                form_inputs_text = parts[1].split("\n")[0].strip()

        res = "🤖 **AI Copilot Helper**\n\n"

        if matched_tool_key:
            tool_info = tools_db[matched_tool_key]
            res += f"📌 **Tool:** {tool_info['name']}\n"
            res += f"{tool_info['description']}\n\n"

            if form_inputs_text and form_inputs_text != "No custom form parameters entered yet":
                res += f"🔍 **Your Active Setup:**\n`{form_inputs_text}`\n\n"
            else:
                res += f"🔍 **Setup Status:** No custom inputs entered yet. Type your target details in the fields above.\n\n"

            res += f"💻 **Quick Example Command:**\n`{tool_info['usage']}`\n\n"
            res += f"🛡️ **Security Recommendation:**\n{tool_info['advice']}\n\n"
        elif user_prompt:
            res += f"❓ **Answer:**\n"
            res += f"Regarding *\"{user_prompt}\"*: Ensure target parameters match your scope of authorization before running tests.\n\n"
        else:
            res += "🔍 **Setup Status:** Ready. Select any security tool above and configure target details.\n\n"

        return res



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
