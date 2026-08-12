import os
import shlex
import subprocess
import shutil
import random
# pyrefly: ignore [missing-import]
from PyQt6.QtCore import QThread, pyqtSignal
from datetime import datetime
import time

from core.log_manager import LogManager
from core.port_parser import PortParser
from core.risk_engine import RiskEngine
from core.suggestion_engine import SuggestionEngine
from core.app_state import app_state
from core.database import DatabaseManager
from core.pipeline_manager import PipelineManager



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

    def run(self):
        try:
            command_args = shlex.split(self.command, posix=os.name != "nt")
            if not command_args:
                raise ValueError("No command provided.")

            # Log command
            LogManager.log_command(self.command)
            self.start_time = time.time()

            # Extract tool name from command
            tool_binary = command_args[0].lower()
            tool_name = command_args[0].upper()
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
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
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
                "  /_/   /_/ /_/\____/\\__/\____/_/ /_/ v1.2.2",
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
