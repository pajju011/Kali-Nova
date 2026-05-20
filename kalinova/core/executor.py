import os
import shlex
import subprocess
import shutil
import random
from PyQt6.QtCore import QThread, pyqtSignal
from datetime import datetime
import time

from core.log_manager import LogManager
from core.port_parser import PortParser
from core.risk_engine import RiskEngine
from core.suggestion_engine import SuggestionEngine
from core.app_state import app_state


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
                    self.output_signal.emit(f"Tool exited with code: {process.returncode}")
                    self.status_signal.emit(f"{tool_name} failed", "error")
                self.output_signal.emit(f"{'='*60}\n")

            # Calculate risk after execution
            RiskEngine.calculate()

            # Generate suggestions
            SuggestionEngine.generate()

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
