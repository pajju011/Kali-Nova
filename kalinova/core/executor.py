import os
import shlex
import subprocess
import shutil
import random
# pyrefly: ignore [missing-import]
from PyQt6.QtCore import QThread, pyqtSignal
from datetime import datetime
import time

from config import load_config
from core.log_manager import LogManager
from core.port_parser import PortParser
from core.risk_engine import RiskEngine
from core.suggestion_engine import SuggestionEngine
from core.app_state import app_state
from core.database import DatabaseManager
from core.pipeline_manager import PipelineManager
from core.system_utils import wrap_with_privilege_escalation, needs_root_privileges



class CommandThread(QThread):

    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    status_signal = pyqtSignal(str, str)  # (status_text, status_type)

    def __init__(self, command):
        super().__init__()
        self.command = command
        self.start_time = None
        self.line_count = 0
        self._process = None
        self._stop_requested = False
        self.stdout_lines = []

    def stop(self):
        self._stop_requested = True
        if self._process is not None and self._process.poll() is None:
            try:
                self._process.terminate()
            except Exception:
                pass

    def send_input(self, text: str):
        """Sends interactive user input/keystrokes to the running subprocess stdin."""
        if self._process is not None and self._process.poll() is None:
            if self._process.stdin is not None:
                try:
                    self._process.stdin.write(f"{text}\n")
                    self._process.stdin.flush()
                    self.output_signal.emit(f"> [INPUT] {text}")
                except Exception as e:
                    self.output_signal.emit(f"[ERROR] Failed to send stdin input: {e}")
            else:
                self.output_signal.emit("[WARN] stdin stream is not open for this process.")
        else:
            self.output_signal.emit(f"> [INPUT] {text} (No active subprocess)")

    def run(self):
        try:
            # Check privilege escalation configuration
            config = load_config()
            auto_elevate = config.get("auto_elevate_root", True)
            elevation_method = config.get("elevation_method", "auto")

            exec_cmd = self.command
            if auto_elevate and elevation_method != "none":
                elevated_cmd, was_elevated = wrap_with_privilege_escalation(
                    self.command, method=elevation_method
                )
                if was_elevated:
                    self.output_signal.emit(f"[PRIVILEGE] Executing with elevated permissions ({elevation_method})...\n")
                    exec_cmd = elevated_cmd

            command_args = shlex.split(exec_cmd, posix=os.name != "nt")
            if not command_args:
                raise ValueError("No command provided.")

            # Log command
            LogManager.log_command(self.command)
            self.start_time = time.time()

            # Extract tool name from command
            tool_binary = command_args[0].lower()
            if tool_binary in {"sudo", "pkexec"} and len(command_args) > 1:
                tool_binary = command_args[1].lower()
            tool_name = tool_binary.upper()
            self.status_signal.emit(f"Running {tool_name}...", "running")
            self.output_signal.emit(f"\n{'='*60}")
            self.output_signal.emit(f"Starting: {self.command}")
            self.output_signal.emit(f"{'='*60}\n")

            # Check if command binary is installed
            base_binary = os.path.basename(tool_binary)
            if base_binary.endswith(".exe"):
                base_binary = base_binary[:-4]
            
            is_installed = shutil.which(base_binary) is not None

            if not is_installed:
                # Fallback to simulation
                self.output_signal.emit(f"[INFO] '{base_binary}' tool not detected locally. Running in Simulation Mode...\n")
                self.run_simulation(base_binary, command_args)
            else:
                startupinfo = None
                creationflags = 0
                if os.name == "nt":
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    creationflags = subprocess.CREATE_NO_WINDOW

                process = subprocess.Popen(
                    command_args,
                    shell=False,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    startupinfo=startupinfo,
                    creationflags=creationflags,
                )
                self._process = process

                for line in process.stdout:
                    if self._stop_requested:
                        break
                    clean = line.strip()
                    if clean:  # Only emit non-empty lines
                        self.process_output_line(clean)

                process.wait()
                
                # Calculate execution time
                elapsed_time = time.time() - self.start_time
                
                self.output_signal.emit(f"\n{'='*60}")
                if self._stop_requested:
                    self.output_signal.emit("Tool execution stopped by user.")
                    self.status_signal.emit(f"{tool_name} stopped", "info")
                elif process.returncode == 0:
                    self.output_signal.emit("Tool completed successfully!")
                    self.output_signal.emit(f"Execution time: {elapsed_time:.2f}s | Lines: {self.line_count}")
                    self.status_signal.emit(f"{tool_name} completed ({elapsed_time:.1f}s)", "success")
                else:
                    self.output_signal.emit(f"[INFO] Real tool '{base_binary}' exited with code: {process.returncode}. Switching to Simulation Mode...\n")
                    self.run_simulation(base_binary, command_args)
                    return
                self.output_signal.emit(f"{'='*60}\n")

            # Extract target from command args
            target = "unknown"
            if len(command_args) > 1:
                # Find target by filtering out flags/options
                for arg in command_args[1:]:
                    if not arg.startswith("-"):
                        target = arg
                        break

            # Ingest output into pipeline manager for inter-tool data handoff
            PipelineManager.ingest_output(base_binary, "\n".join(self.stdout_lines), target)
            app_state.record_tool_execution(base_binary, target, self.command)

            # Calculate risk after execution
            RiskEngine.calculate()

            # Generate suggestions & ML recommendations
            SuggestionEngine.generate()

            # Save scan to database
            parsed_ports_str = ",".join(map(str, app_state.open_ports))
            DatabaseManager.save_scan(
                target=target,
                tool_name=tool_name,
                command=self.command,
                stdout="\n".join(self.stdout_lines),
                parsed_ports=parsed_ports_str,
                risk_score=app_state.risk_score,
                threat_level=app_state.global_risk
            )

        except Exception as e:
            self.output_signal.emit(f"\nERROR: {str(e)}")
            self.status_signal.emit("Error executing tool", "error")
            LogManager.log_output(str(e))
        finally:
            self._process = None

        self.finished_signal.emit()

    def process_output_line(self, clean):
        self.output_signal.emit(clean)
        self.line_count += 1
        self.stdout_lines.append(clean)

        LogManager.log_output(clean)
        PortParser.extract_ports(clean)

        # ========================
        # 🔥 EVENT DETECTION
        # ========================

        lower_line = clean.lower()

        # SQL Injection Detection
        if "sql injection" in lower_line:
            app_state.add_event("SQL_INJECTION")
            self.output_signal.emit("[ALERT] SQL Injection vulnerability detected!")

        # Hydra / Brute Force Detection
        if "hydra" in lower_line or "login:" in lower_line:
            app_state.add_event("BRUTE_FORCE")
            self.output_signal.emit("[ALERT] Brute force attempt detected!")

        # Gobuster Directory Enumeration
        if "found:" in lower_line:
            app_state.add_event("DIR_ENUM")

        # Email Enumeration (Harvester)
        if "@" in clean and "." in clean and len(clean) > 5:
            app_state.add_event("EMAIL_ENUM")

        # Wireless Handshake / Wifite Detection
        if "captured" in lower_line and ("handshake" in lower_line or "pmkid" in lower_line):
            app_state.add_event("WIRELESS_HANDSHAKE")
            self.output_signal.emit("[ALERT] Wireless handshake/PMKID captured!")

        # Autopsy Digital Forensics Detection
        if "autopsy forensic browser" in lower_line or "evidence locker" in lower_line:
            app_state.add_event("FORENSICS_ANALYSIS")
            self.output_signal.emit("[INFO] Digital forensics session initiated!")

        # Wash / Reaver WPS Detection
        if "wps" in lower_line and ("bssid" in lower_line or "pin" in lower_line or "reaver" in lower_line or "wash" in lower_line):
            app_state.add_event("WPS_WIFI_AUDIT")

        # Photon OSINT Crawl Detection
        if "photon" in lower_line or "crawling" in lower_line or "urls extracted" in lower_line:
            app_state.add_event("OSINT_CRAWL")
            self.output_signal.emit("[INFO] OSINT Web Crawl session active.")

        if "secret key" in lower_line or "secret_leak" in lower_line or "[!] secret" in lower_line or "api_key" in lower_line:
            app_state.add_event("SECRET_LEAK")
            self.output_signal.emit("[ALERT] Secret API key or sensitive token detected during Photon crawl!")

        if "subdomain discovered" in lower_line or "subdomain found" in lower_line:
            app_state.add_event("SUBDOMAIN_ENUM")
            self.output_signal.emit("[INFO] Subdomain discovered during web crawl.")

        # Metagoofil Document & Metadata Detection
        if "metagoofil" in lower_line or "searching for pdf files" in lower_line or "files found" in lower_line:
            app_state.add_event("METAGOOFIL_DOC_EXTRACT")
            self.output_signal.emit("[INFO] Metagoofil document search & metadata extraction active.")

        # Amass DNS Enumeration & Attack Surface Detection
        if "amass" in lower_line or "owasp amass" in lower_line or "querying" in lower_line or "dns enumeration" in lower_line:
            app_state.add_event("AMASS_ENUM_ACTIVE")
            self.output_signal.emit("[INFO] OWASP Amass attack surface discovery active.")

        # Hashcat Password Cracking Detection
        if "hashcat" in lower_line or "hashmode:" in lower_line or "speed.#" in lower_line or "dictionary cache hit" in lower_line:
            app_state.add_event("HASH_CRACKING_ACTIVE")
            if "recovered" in lower_line or "cracked" in lower_line:
                self.output_signal.emit("[ALERT] Hashcat hash plaintext recovered!")

        # Ncrack Network Authentication & Credential Discovery Detection
        if "ncrack" in lower_line or "discovered credentials on" in lower_line:
            app_state.add_event("BRUTE_FORCE")
            app_state.add_event("NCRACK_CREDENTIAL_FOUND")
            if "discovered credentials on" in lower_line:
                self.output_signal.emit("[ALERT] Ncrack discovered valid service credentials!")

    def run_simulation(self, tool_binary, command_args):
        simulated_lines = []
        target = "target-system.local"
        if len(command_args) > 1:
            for arg in command_args[1:]:
                if not arg.startswith("-"):
                    target = arg
                    break

        if tool_binary == "nmap":
            simulated_lines = [
                f"Starting Nmap 7.92 ( https://nmap.org ) at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"Nmap scan report for {target}",
                "Host is up (0.0051s latency).",
                "Not shown: 996 closed tcp ports (conn-refused)",
                "PORT     STATE SERVICE",
                "22/tcp   open  ssh",
                "80/tcp   open  http",
                "443/tcp  open  https",
                "8080/tcp open  http-proxy",
                "MAC Address: 00:0C:29:3E:B2:A1 (VMware)",
                "Device type: general purpose",
                "Running: Linux 5.X",
                "OS CPE: cpe:/o:linux:linux_kernel:5",
                "OS details: Linux 5.0 - 5.4",
                f"Nmap done: 1 IP address (1 host up) scanned in {random.uniform(2.1, 4.5):.2f} seconds"
            ]

        elif tool_binary == "whois":
            simulated_lines = [
                f"Domain Name: {target.upper()}",
                "Registry Domain ID: 234567890_DOMAIN_COM-VRSN",
                "Registrar WHOIS Server: whois.verisign-grs.com",
                "Registrar URL: http://www.registrar-example.com",
                "Updated Date: 2026-01-15T10:00:00Z",
                "Creation Date: 2005-04-20T04:00:00Z",
                "Registry Expiry Date: 2028-04-20T04:00:00Z",
                "Registrar: Registrar Example LLC",
                "Domain Status: clientTransferProhibited https://icann.org/epp#clientTransferProhibited",
                "Registrant Name: IT Security Sandbox",
                "Registrant Organization: Security Testing Sandbox Ltd.",
                "Registrant State/Province: CA",
                "Registrant Country: US",
                "Name Server: NS1.SANDBOX.COM",
                "Name Server: NS2.SANDBOX.COM",
                "DNSSEC: unsigned",
                "<<< Last update of WHOIS database: 2026-05-20T23:16:00Z >>>"
            ]

        elif "harvester" in tool_binary or "theharvester" in tool_binary:
            source = "google"
            if "-b" in command_args:
                try:
                    idx = command_args.index("-b")
                    source = command_args[idx+1]
                except Exception:
                    pass
            simulated_lines = [
                "*******************************************************************************",
                "*  theHarvester 4.0.3                                                         *",
                "*  Coded by Christian Martorella                                              *",
                "*  Edge-Security Research                                                     *",
                "*******************************************************************************",
                f"[*] Targeting {target}",
                f"[*] Searching {source} ...",
                "[*] Users found: 0",
                "[*] Emails found:",
                f"[-] admin@{target}",
                f"[-] info@{target}",
                f"[-] support@{target}",
                f"[-] database-admin@{target}",
                "[*] Hosts found: 4",
                f"[-] mail.{target} (192.168.1.10)",
                f"[-] vpn.{target} (192.168.1.11)",
                f"[-] dev.{target} (192.168.1.12)",
                f"[-] internal.{target} (10.0.4.5)",
                "[*] Search complete."
            ]

        elif tool_binary == "nikto":
            simulated_lines = [
                f"- Nikto v2.1.6",
                "---------------------------------------------------------------------------",
                f"+ Target IP:          192.168.1.45",
                f"+ Target Hostname:    {target}",
                f"+ Target Port:        80",
                "---------------------------------------------------------------------------",
                "+ GET /: The anti-clickjacking X-Frame-Options header is not present.",
                "+ GET /: The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against certain forms of XSS.",
                "+ GET /: The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type.",
                "+ OSVDB-3092: /admin/: This directory is password protected or accessible without authorization.",
                "+ OSVDB-3268: /images/: Directory indexing found.",
                "+ OSVDB-3233: /config.php: Found sensitive configuration file containing database passwords.",
                "+ OSVDB-3092: /login: Admin access panel detected.",
                "+ 7748 requests tested on local host.",
                "+ Nikto scan completed successfully."
            ]

        elif tool_binary == "sqlmap":
            simulated_lines = [
                "        ___",
                "       __H__",
                "  ___ ___[']_____ ___ ___  {1.6.2#stable}",
                " |_ -| . [']     | .'| . |",
                " |___|_  [.]_|_|_|__,|  _|",
                "     |_|             |_|   https://sqlmap.org",
                "",
                f"[*] starting at {datetime.now().strftime('%H:%M:%S')}",
                "",
                "[INFO] testing connection to the target URL",
                "[INFO] checking if the target is protected by some WAF/IPS",
                "[INFO] testing if the url parameter 'id' is vulnerable to SQL injection",
                "[INFO] heuristic test shows that GET parameter 'id' might be injectable",
                "[ALERT] SQL injection vulnerability detected on parameter 'id'!",
                "[INFO] confirming injection technique (UNION query)",
                "[INFO] GET parameter 'id' is vulnerable! Extraction of schema is possible.",
                "[INFO] actively dump database metadata...",
                "Database: kalinova_db",
                "Table: users",
                "[2 columns]",
                "+----------+-------------+",
                "| Column   | Type        +",
                "+----------+-------------+",
                "| id       | int(11)     |",
                "| password | varchar(64) |",
                "+----------+-------------+",
                "[INFO] Dumped 1 table to CSV successfully."
            ]

        elif tool_binary == "gobuster":
            wordlist = "common.txt"
            if "-w" in command_args:
                try:
                    idx = command_args.index("-w")
                    wordlist = os.path.basename(command_args[idx+1])
                except Exception:
                    pass
            simulated_lines = [
                "===============================================================",
                "Gobuster v3.1.0",
                "by OJ Reeves (@TheColonial)",
                "===============================================================",
                f"[+] Url:                     {target}",
                "[+] Method:                  GET",
                f"[+] Wordlist:                {wordlist}",
                "[+] Negative Status:         404",
                "===============================================================",
                f"{datetime.now().strftime('%Y/%m/%d %H:%M:%S')} Starting gobuster in directory brute-forcing mode",
                "===============================================================",
                "/admin               (Status: 200) [Size: 1242]",
                "/login               (Status: 200) [Size: 840]",
                "/uploads             (Status: 301) [Size: 312] (Redirect to: /uploads/)",
                "/config.php          (Status: 200) [Size: 0]",
                "/secret              (Status: 403) [Size: 280]",
                "/backup              (Status: 301) [Size: 220]",
                "===============================================================",
                f"{datetime.now().strftime('%Y/%m/%d %H:%M:%S')} Finished",
                "==============================================================="
            ]

        elif tool_binary == "hydra":
            username = "admin"
            if "-l" in command_args:
                try:
                    idx = command_args.index("-l")
                    username = command_args[idx+1]
                except Exception:
                    pass
            simulated_lines = [
                "Hydra v9.3 (c) 2026 by van Hauser/THC - Please play responsibly and use legally",
                f"[DATA] attacking ssh://{target}:22/",
                "[STATUS] attack started with 16 parallel tasks",
                "[STATUS] 100 passwords tried, progress 12%",
                "[STATUS] 200 passwords tried, progress 24%",
                "[STATUS] 300 passwords tried, progress 36%",
                "[STATUS] 400 passwords tried, progress 48%",
                "[ALERT] Brute force attempt detected!",
                f"[22][ssh] host: {target}   login: {username}   password: admin",
                "[STATUS] attack finished. 1 target successfully cracked."
            ]

        elif tool_binary == "john":
            hash_file = "hashes.txt"
            if len(command_args) > 1:
                hash_file = os.path.basename(command_args[1])
            simulated_lines = [
                "Created directory: $JOHN/",
                "Using default input encoding: UTF-8",
                f"Loaded 1 password hash ({hash_file}) (SHA-256, crypt)",
                "Will reject shorter passwords than 4",
                "Press 'q' or Ctrl-C to abort, almost any other key for status",
                "admin123         (admin)",
                "1 password hash cracked, 0 left"
            ]

        elif tool_binary == "ncrack":
            user = "victim"
            if "--user" in command_args:
                try:
                    user = command_args[command_args.index("--user") + 1]
                except Exception:
                    pass
            elif "-U" in command_args:
                try:
                    user = os.path.basename(command_args[command_args.index("-U") + 1])
                except Exception:
                    pass

            svc = "rdp"
            if "-p" in command_args:
                try:
                    svc = command_args[command_args.index("-p") + 1]
                except Exception:
                    pass

            target_host = target if target != "unknown" and target != "target-system.local" else "192.168.1.200"
            if "-iL" in command_args:
                try:
                    target_host = f"list:{os.path.basename(command_args[command_args.index('-iL') + 1])}"
                except Exception:
                    pass

            port_map = {"rdp": "3389", "ssh": "22", "ftp": "21", "smb": "445", "vnc": "5900", "http": "80", "telnet": "23"}
            svc_port = port_map.get(svc.lower(), "3389")

            simulated_lines = [
                f"Starting Ncrack 0.7 ( http://ncrack.org ) at {datetime.now().strftime('%Y-%m-%d %H:%M EDT')}",
                f"[*] Initiating network authentication audit against {target_host} ({svc} / port {svc_port})",
                f"[*] Module {svc}: parallel connection limit set. Probing endpoint...",
                f"{svc}://192.168.1.220:{svc_port} finished.",
                f"Discovered credentials on {svc}://192.168.1.200:{svc_port} '{user}' 's3cr3t'",
                f"Ncrack done: 1 service on 1 host completed in {random.uniform(3.2, 5.8):.2f} seconds."
            ]

        elif tool_binary in ["nc", "netcat"]:
            port = "4444"
            if len(command_args) > 2:
                port = command_args[-1]
            simulated_lines = [
                f"Listening on [0.0.0.0] (family 2, port {port})",
                "Connection from 192.168.1.104 received!",
                "$ id",
                "uid=1000(kali) gid=1000(kali) groups=1000(kali)",
                "$ whoami",
                "kali",
                "$ hostname",
                "target-system-secured",
                "$ ls -la",
                "total 12",
                "drwxr-xr-x 2 kali kali 4096 May 20 23:00 .",
                "drwxr-xr-x 3 root root 4096 May 20 22:50 ..",
                "-rw-r--r-- 1 kali kali   32 May 20 23:00 flag.txt"
            ]

        elif tool_binary == "wireshark":
            simulated_lines = [
                "Capturing live packets on interface 'eth0'...",
                "[1] TCP 192.168.1.45 -> 192.168.1.100 [SYN] Seq=0 Win=64240 Len=0",
                "[2] TCP 192.168.1.100 -> 192.168.1.45 [SYN, ACK] Seq=0 Ack=1 Win=65535 Len=0",
                "[3] TCP 192.168.1.45 -> 192.168.1.100 [ACK] Seq=1 Ack=1 Win=64240 Len=0",
                "[4] HTTP GET /admin HTTP/1.1",
                "[5] HTTP HTTP/1.1 401 Unauthorized",
                "[6] TCP 192.168.1.45 -> 192.168.1.100 [FIN, ACK] Seq=1 Ack=2 Win=64240 Len=0",
                "Capture completed. 6 packets parsed successfully."
            ]

        elif tool_binary == "wifite":
            simulated_lines = [
                "   .               .    ",
                " .´  ·  .     .  ·  `.  wifite2 2.8.1",
                " :  :  :  (¯)  :  :  :  a wireless auditor by derv82",
                " `.  ·  ` /¯\\ ´  ·  .´  maintained by kimocoder",
                "   `     /¯¯¯\\     ´    https://github.com/kimocoder/wifite2",
                "",
                "[+] enabling monitor mode on wlan0... enabled as wlan0mon",
                "[+] scanning for wireless targets (press Ctrl+C when ready)",
                " NUM                  ESSID   CH  ENCR  POWER  CLIENTS",
                " ---  ---------------------  ---  ----  -----  -------",
                "   1           Corp_Office_5G   36   WPA2    85%        3",
                "   2           Guest_Network     6   WPA2    62%        1",
                "   3          Legacy_IoT_AP      1    WEP    45%        0",
                "[+] select target(s) (1-3) or type all: 1",
                "[+] targeting Corp_Office_5G (00:11:22:33:44:55)",
                "[+] listening for PMKID... captured PMKID for Corp_Office_5G!",
                "[+] deauthenticating clients to capture WPA handshake...",
                "[+] captured WPA handshake for Corp_Office_5G!",
                "[+] saved handshake to hs/Corp_Office_5G_00-11-22-33-44-55.cap",
                "[+] cracking handshake using wordlist...",
                "[+] KEY FOUND! [ CorporatePass2026! ]",
                "[+] 1 attack completed, 1 handshake captured, 1 key cracked."
            ]

        elif tool_binary == "autopsy":
            port = "9999"
            if "-p" in command_args:
                try:
                    idx = command_args.index("-p")
                    port = command_args[idx+1]
                except Exception:
                    pass
            simulated_lines = [
                "===============================================================================",
                "Autopsy Forensic Browser v2.24",
                "The Sleuth Kit Graphical Interface for Digital Forensics Analysis",
                "===============================================================================",
                "[+] Evidence Locker Directory: /var/lib/autopsy",
                f"[+] Starting Autopsy HTTP Server on port {port}...",
                "[+] Host binding: localhost",
                "[+] Initializing SleuthKit plugins (tsk_loaddb, fls, mactime, srch_strings)...",
                "[+] Autopsy Forensic Browser server is running!",
                "",
                f"    Open your web browser and navigate to: http://localhost:{port}/autopsy",
                "",
                "[+] Waiting for incoming browser connection..."
            ]

        elif tool_binary == "wash":
            simulated_lines = [
                "BSSID               Ch  dBm  WPS  Lck  Vendor    ESSID",
                "--------------------------------------------------------------------------------",
                "E0:3F:49:6A:57:78    6  -73  1.0  No   Unknown   ASUS",
                "00:14:6C:7E:40:80   11  -65  2.0  No   TP-Link   NETGEAR_WPS",
                "[+] Wash scan complete. 2 WPS-enabled Access Points detected."
            ]

        elif tool_binary == "reaver":
            bssid = "E0:3F:49:6A:57:78"
            if "-b" in command_args:
                try:
                    idx = command_args.index("-b")
                    bssid = command_args[idx+1]
                except Exception:
                    pass
            simulated_lines = [
                "Reaver v1.6.5 WiFi Protected Setup (WPS) Attack Tool",
                "Copyright (c) 2011, Tactical Network Solutions, Craig Heffner <cheffner@tacnetsol.com>",
                "",
                f"[+] Waiting for beacon from {bssid}",
                f"[+] Associated with {bssid} (ESSID: ASUS)",
                "[+] Trying WPS pin 12345670",
                "[+] Trying WPS pin 23456781",
                "[+] Trying WPS pin 34567892",
                f"[+] WPS PIN '34567892' successfully cracked for BSSID {bssid}!",
                "[+] WPA PSK: 'WirelessSecure2026!'",
                "[+] Reaver attack completed successfully."
            ]

        elif tool_binary == "photon":
            level = "2"
            threads = "10"
            if "-l" in command_args:
                try:
                    level = command_args[command_args.index("-l") + 1]
                except Exception:
                    pass
            if "-t" in command_args:
                try:
                    threads = command_args[command_args.index("-t") + 1]
                except Exception:
                    pass

            simulated_lines = [
                "      ____  __          __",
                "     / __ \\/ /_  ____  / /_____  ____",
                "    / /_/ / __ \\/ __ \\/ __/ __ \\/ __ \\",
                "   / ____/ / / / /_/ / /_/ /_/ / / / /",
                "  /_/   /_/ /_/\\____/\\__/\\____/_/ /_/ v1.2.2",
                "",
                f"[+] Root target URL: {target}",
                f"[+] Initializing crawler threads (level: {level}, threads: {threads})...",
            ]

            if "--ninja" in command_args:
                simulated_lines.append("[+] Stealth/Ninja mode active: HTTP headers randomized.")
            if "-c" in command_args:
                simulated_lines.append("[+] Custom HTTP Cookie set.")
            if "--user-agent" in command_args:
                simulated_lines.append("[+] Custom User-Agent header applied.")
            if "-o" in command_args:
                try:
                    out_dir = command_args[command_args.index("-o") + 1]
                    simulated_lines.append(f"[+] Output directory configured: {out_dir}")
                except Exception:
                    pass

            simulated_lines.extend([
                "[+] Crawling URLs (in-scope & out-of-scope)...",
                f"[-] Found internal endpoint: {target}/gallery.php?id=2",
                f"[-] Found internal endpoint: {target}/api/v1/users",
                "[*] Extracting OSINT intelligence...",
                f"[-] Email discovered: admin@{target.replace('http://', '').replace('https://', '')}",
                f"[-] Email discovered: security@{target.replace('http://', '').replace('https://', '')}",
                "[-] Subdomain discovered: api.sandbox.local",
                "[-] Subdomain discovered: dev-portal.sandbox.local"
            ])

            if "--wayback" in command_args:
                simulated_lines.append("[+] Wayback Machine seed URLs retrieved.")

            if "-r" in command_args:
                simulated_lines.append("[+] Custom regex pattern matches extracted from response bodies.")

            if "--keys" in command_args or True:
                simulated_lines.append("[!] Secret key detected in app.js: 'AKIAIOSFODNN7EXAMPLE'")

            if "--clone" in command_args:
                simulated_lines.append("[+] Local website mirror cloned successfully.")

            simulated_lines.append("[+] Crawl finished. Extracted 42 URLs, 2 emails, 2 subdomains, 1 secret key.")

        elif tool_binary == "metagoofil":
            domain = target
            if "-d" in command_args:
                try:
                    domain = command_args[command_args.index("-d") + 1]
                except Exception:
                    pass
            filetypes = "pdf"
            if "-t" in command_args:
                try:
                    filetypes = command_args[command_args.index("-t") + 1]
                except Exception:
                    pass
            limit = "100"
            if "-l" in command_args:
                try:
                    limit = command_args[command_args.index("-l") + 1]
                except Exception:
                    pass
            download_limit = "25"
            if "-n" in command_args:
                try:
                    download_limit = command_args[command_args.index("-n") + 1]
                except Exception:
                    pass
            out_dir = "kalipdf"
            if "-o" in command_args:
                try:
                    out_dir = command_args[command_args.index("-o") + 1]
                except Exception:
                    pass
            save_file = "kalipdf.html"
            if "-f" in command_args:
                try:
                    save_file = command_args[command_args.index("-f") + 1]
                except Exception:
                    pass

            simulated_lines = [
                "******************************************************",
                "*     /\\/\\   ___| |_ __ _  __ _  ___   ___  / _(_) | *",
                "*    /    \\ / _ \\ __/ _` |/ _` |/ _ \\ / _ \\| |_| | | *",
                "*   / /\\/\\ \\  __/ || (_| | (_| | (_) | (_) |  _| | | *",
                "*   \\/    \\/\\___|\\__\\__,_|\\__, |\\___/ \\___/|_| |_|_| *",
                "*                         |___/                      *",
                "* Metagoofil Ver 2.2                                 *",
                "* Christian Martorella                               *",
                "* Edge-Security.com                                  *",
                "* cmartorella_at_edge-security.com                   *",
                "******************************************************",
                f"['{filetypes}']",
                "",
                "[-] Starting online search...",
                f"[-] Searching for {filetypes} files, with a limit of {limit}",
                f"        Searching {limit} results...",
                "Results: 21 files found",
                f"Starting to download {download_limit} of them:",
                f"[-] [1/21] Downloading http://{domain}/docs/annual_report_2025.pdf",
                f"[-] [2/21] Downloading http://{domain}/assets/network_topology_spec.pdf",
                f"[-] [3/21] Downloading http://{domain}/downloads/employee_handbook.pdf",
                f"[+] Saving document links output to '{save_file}'",
                "[+] Extracting document metadata (Author, Software, Title, Creator)...",
                "    Author found: admin_jsmith (Internal Account)",
                "    Creator/Producer: Microsoft Office Word 2019 / Acrobat Distiller 11",
                "    Internal Path: C:\\Users\\jsmith\\Documents\\Confidential\\",
                f"[-] Saved downloaded files to directory '{out_dir}'.",
                "[-] Metagoofil metadata extraction completed successfully."
            ]

        elif tool_binary == "amass":
            domain = target
            if "-d" in command_args:
                try:
                    domain = command_args[command_args.index("-d") + 1]
                except Exception:
                    pass
            mode = "enum"
            if "intel" in command_args:
                mode = "intel"

            simulated_lines = [
                "                                       ",
                "  .____.     .____.    .____.    .____.",
                "  |    |     |    |    |    |    |    |",
                "  | OWASP Amass v4.2.0 - Attack Surface Mapping Engine |",
                "  |____________________________________________________|",
                "",
                f"[*] Target Domain: {domain}",
                f"[*] Operation Mode: {mode.upper()}",
                "[+] Querying passive OSINT sources (Censys, CertSpotter, Crtsh, HackerTarget, SecurityTrails, Shodan, VirusTotal)...",
                f"[-] [Crtsh] Found subdomain: mail.{domain}",
                f"[-] [SecurityTrails] Found subdomain: vpn.{domain}",
                f"[-] [AlienVault] Found subdomain: api.{domain}",
                f"[-] [Censys] Found subdomain: dev.{domain}",
                f"[-] [HackerTarget] Found subdomain: portal.{domain}",
            ]

            if "-active" in command_args or "--active" in command_args:
                simulated_lines.extend([
                    "[+] Active reconnaissance mode enabled: Probing DNS zone transfers (AXFR) & SSL/TLS Certificates...",
                    f"[-] [DNS AXFR] Discovered internal DNS record: ns1.internal.{domain}",
                    f"[-] [Cert Pull] Discovered SSL SAN endpoint: staging-api.{domain}"
                ])

            if "-brute" in command_args or "--brute" in command_args:
                simulated_lines.extend([
                    "[+] Brute-force subdomain alterations & wordlist mutations active...",
                    f"[-] [BruteForce] Found subdomain: admin.{domain}",
                    f"[-] [BruteForce] Found subdomain: db.{domain}"
                ])

            if "-ip" in command_args or "--ip" in command_args or True:
                simulated_lines.extend([
                    "[+] Performing A/AAAA DNS records resolution to IPv4/IPv6 addresses:",
                    f"    mail.{domain}        --> 192.168.1.10 [ASN: 15169 - GOOGLE]",
                    f"    vpn.{domain}         --> 192.168.1.15 [ASN: 15169 - GOOGLE]",
                    f"    api.{domain}         --> 192.168.1.25 [ASN: 15169 - GOOGLE]",
                    f"    portal.{domain}      --> 192.168.1.30 [ASN: 15169 - GOOGLE]",
                    f"    dev.{domain}         --> 192.168.1.45 [ASN: 15169 - GOOGLE]",
                ])

            if "-src" in command_args:
                simulated_lines.append("[+] Data source attribution logging enabled.")

            simulated_lines.append(f"[*] OWASP Amass discovery complete. 7 subdomains and 5 unique IP targets mapped.")

        elif tool_binary == "hashcat":
            if "-b" in command_args or "--benchmark" in command_args:
                simulated_lines = [
                    "hashcat (v7.1.2) starting in benchmark mode...",
                    "",
                    "Benchmarking uses hand-optimized kernel code by default.",
                    "You can use it in your cracking session by setting the -O option.",
                    "",
                    "OpenCL Platform #1: Intel(R) Corporation",
                    "========================================",
                    "* Device #1: Intel(R) Core(TM) i7 CPU @ 3.40GHz, 4096/16384 MB allocatable",
                    "",
                    "Benchmark relevant options:",
                    "===========================",
                    "* --optimized-kernel-enable",
                    "",
                    "Hashmode: 0 - MD5",
                    "Speed.#1.........:   134.9 MH/s (15.41ms) @ Accel:1024 Loops:1024 Thr:1 Vec:8",
                    "",
                    "Hashmode: 100 - SHA1",
                    "Speed.#1.........: 98899.4 kH/s (21.04ms) @ Accel:1024 Loops:1024 Thr:1 Vec:8",
                    "",
                    "Hashmode: 500 - md5crypt, MD5 (Unix), Cisco-IOS $1$ (MD5)",
                    "Speed.#1.........:   18400 H/s (24.10ms) @ Accel:512 Loops:256 Thr:1 Vec:8",
                    "",
                    "Hashmode: 1000 - NTLM",
                    "Speed.#1.........:  425.2 MH/s (12.10ms) @ Accel:1024 Loops:1024 Thr:1 Vec:8",
                    "",
                    "Hashmode: 1400 - SHA2-256",
                    "Speed.#1.........: 42768.3 kH/s (48.86ms) @ Accel:1024 Loops:1024 Thr:1 Vec:8",
                    "",
                    "Benchmark completed."
                ]
            else:
                hash_target = "$1$uOM6WNc4$r3ZGeSB11q6UUSILqek3J1"
                wordlist = "/usr/share/wordlists/rockyou.txt"
                if len(command_args) > 1:
                    for arg in command_args[1:]:
                        if not arg.startswith("-"):
                            if "hash" in arg or "$" in arg or "." in arg:
                                hash_target = arg
                            elif "word" in arg or "dict" in arg or "txt" in arg or "rock" in arg:
                                wordlist = arg

                hash_mode_str = "500 (md5crypt)"
                if "-m" in command_args:
                    try:
                        m_val = command_args[command_args.index("-m") + 1]
                        hash_mode_str = f"{m_val}"
                    except Exception:
                        pass

                simulated_lines = [
                    "hashcat (v7.1.2) starting...",
                    "",
                    "OpenCL Platform #1: Intel(R) Corporation",
                    "========================================",
                    "* Device #1: Intel(R) Core(TM) i7 CPU @ 3.40GHz, 4096/16384 MB allocatable",
                    "",
                    "Hashes: 1 digests; 1 unique digests, 1 unique salts",
                    "Applicable optimizers:",
                    "* Zero-Byte",
                    "* Single-Hash",
                    "* Single-Salt",
                    "",
                    f"Dictionary cache hit:",
                    f"* Filename..: {wordlist}",
                    "* Passwords.: 1406529",
                    "* Bytes.....: 12790573",
                    "* Keyspace..: 1406529",
                    "",
                    "Session..........: hashcat",
                    "Status...........: Running",
                    f"Hash.Type........: Hashmode {hash_mode_str}",
                    f"Hash.Target......: {hash_target}",
                    "Time.Started.....: Sat Nov 24 22:37:25 (26 secs)",
                    "Speed.#1.........:     18400 H/s (9.09ms) @ Accel:256 Loops:125 Thr:1 Vec:8",
                    "Recovered........: 1/1 (100.00%) Digests, 1/1 (100.00%) Salts",
                    "Progress.........: 183808/1406529 (13.07%)",
                    "",
                    f"[+] KEY FOUND! Plaintext password recovered: [ admin123! ]",
                    "Session completed successfully."
                ]

        else:
            simulated_lines = [
                f"Executing simulated {tool_binary} script...",
                f"Scanning active target: {target}",
                "Processing payload data...",
                "Task completed successfully."
            ]

        for line in simulated_lines:
            if self._stop_requested:
                break
            self.process_output_line(line)
            time.sleep(random.uniform(0.08, 0.20))

        elapsed_time = time.time() - self.start_time
        self.output_signal.emit(f"\n{'='*60}")
        if self._stop_requested:
            self.output_signal.emit("Tool execution stopped by user.")
            self.status_signal.emit(f"{tool_binary.upper()} stopped", "info")
        else:
            self.output_signal.emit("Simulated tool completed successfully!")
            self.output_signal.emit(f"Execution time: {elapsed_time:.2f}s | Lines: {self.line_count}")
            self.status_signal.emit(f"{tool_binary.upper()} completed ({elapsed_time:.1f}s)", "success")
        self.output_signal.emit(f"{'='*60}\n")
