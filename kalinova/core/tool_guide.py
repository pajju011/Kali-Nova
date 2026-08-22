"""
Tool Usage Guide & Input Format Validator for Kali-Nova.
Provides target validation, syntax guides, flag dictionaries, and tool pipeline chaining logic.
"""

import re
from typing import Dict, Any, Tuple


class ToolGuide:
    """
    Provides real-time target input format validation and flag explanations
    for all supported security tools in Kali-Nova.
    """

    IP_REGEX = re.compile(r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$")
    CIDR_REGEX = re.compile(r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)/(?:[0-9]|[12]\d|3[0-2])$")
    DOMAIN_REGEX = re.compile(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$")
    URL_REGEX = re.compile(r"^https?://[^\s/$.?#].[^\s]*$", re.IGNORECASE)

    TOOL_SCHEMAS: Dict[str, Dict[str, Any]] = {
        "nmap": {
            "name": "Nmap Network Scanner",
            "accepted_inputs": ["IP Address (e.g., 192.168.1.1)", "CIDR Range (e.g., 10.0.0.0/24)", "Domain Name (e.g., scanme.nmap.org)"],
            "input_type": "HOST_OR_NETWORK",
            "flags": {
                "-sV": "Probe open ports to determine service and version information.",
                "-sS": "Stealth TCP SYN scan (half-open scanning, quiet and fast).",
                "-Pn": "Treat all hosts as online (skips ICMP ping probe if blocked by firewall).",
                "-A": "Enable aggressive scanning (OS detection, version detection, script scanning, and traceroute).",
                "-p": "Specify port range (e.g., -p 80,443 or -p 1-1000).",
                "-T4": "Set timing template to aggressive for faster execution on reliable networks."
            },
            "best_practices": "Start with Fast Triage ports (-p 80,443,22,21,3306) with -sV. If ping is blocked, append -Pn.",
            "pipeline_next": ["Nikto", "Gobuster", "Hydra", "Sqlmap"]
        },
        "nikto": {
            "name": "Nikto Web Vulnerability Scanner",
            "accepted_inputs": ["Full URL (e.g., http://example.com)", "Host with Port (e.g., 192.168.1.5:8080)"],
            "input_type": "URL_OR_HOST",
            "flags": {
                "-h": "Target host name, IP, or full URL.",
                "-ssl": "Force SSL/TLS encryption mode for HTTPS endpoints.",
                "-C all": "Scan all known CGI directories.",
                "-Tuning": "Filter scan types (e.g., 1=Info disclosure, 2=Misconfiguration, 3=Information leaks)."
            },
            "best_practices": "Use Nikto to audit missing HTTP security headers (CSP, HSTS) and dangerous default files.",
            "pipeline_next": ["Gobuster", "Sqlmap", "AI Copilot"]
        },
        "sqlmap": {
            "name": "SQLmap Automated Database Injection",
            "accepted_inputs": ["Target URL with query parameters (e.g., http://target.com/page.php?id=1)"],
            "input_type": "URL_WITH_PARAM",
            "flags": {
                "-u": "Target URL with testable parameter (?id=1 or /api/user/1).",
                "--batch": "Never ask for user input, use default behavior automatically.",
                "--dbs": "Enumerate DBMS databases upon successful injection.",
                "--tables": "Enumerate DBMS database tables.",
                "--dump": "Dump DBMS database table entries.",
                "--level": "Level of tests to perform (1-5, default 1). Level 2+ tests cookies, 3+ tests user-agent.",
                "--risk": "Risk of tests to perform (1-3, default 1). Higher risk tests may modify database records."
            },
            "best_practices": "Always ensure the URL contains dynamic parameters (?id=, ?cat=). Start with --batch --dbs.",
            "pipeline_next": ["John the Ripper", "HashID", "AI Copilot"]
        },
        "gobuster": {
            "name": "Gobuster URI & Directory Brute-Forcer",
            "accepted_inputs": ["Base Web URL (e.g., http://192.168.1.10)"],
            "input_type": "URL",
            "flags": {
                "dir": "Directory brute-forcing mode.",
                "-u": "Base target URL to fuzz.",
                "-w": "Path to wordlist file (e.g., /usr/share/wordlists/dirb/common.txt).",
                "-x": "File extensions to search for (e.g., php,txt,html,bak,json).",
                "-t": "Number of concurrent threads (default 10)."
            },
            "best_practices": "Specify relevant file extensions (-x php,html,txt) to discover exposed backup and config files.",
            "pipeline_next": ["Sqlmap", "Nikto", "Hydra"]
        },
        "hydra": {
            "name": "Hydra Network Login Cracker",
            "accepted_inputs": ["Target IP or Hostname with Service Protocol (e.g., 192.168.1.20 ssh)"],
            "input_type": "HOST_AND_SERVICE",
            "flags": {
                "-l": "Single target username (e.g., -l admin).",
                "-L": "Wordlist of usernames (e.g., -L /path/users.txt).",
                "-p": "Single password to test across users.",
                "-P": "Wordlist of passwords (e.g., -P /usr/share/wordlists/rockyou.txt).",
                "-t": "Number of parallel tasks (default 16).",
                "-s": "Specify custom port if service is not on default port."
            },
            "best_practices": "Use realistic usernames (-l root or -l admin) and start with top 1000 passwords to avoid service lockout.",
            "pipeline_next": ["AI Copilot", "Netcat"]
        },
        "whois": {
            "name": "Whois Domain Registrar Query",
            "accepted_inputs": ["Domain Name or Public IP (e.g., google.com or 8.8.8.8)"],
            "input_type": "DOMAIN_OR_IP",
            "flags": {},
            "best_practices": "Use Whois in Phase 1 (Reconnaissance) to identify organizational subnets and name servers.",
            "pipeline_next": ["theHarvester", "Nmap"]
        },
        "theharvester": {
            "name": "theHarvester OSINT Gathering",
            "accepted_inputs": ["Company Domain Name (e.g., targetcorp.com)"],
            "input_type": "DOMAIN",
            "flags": {
                "-d": "Domain or company name to search.",
                "-b": "Data source (google, bing, duckduckgo, crtsh, all).",
                "-l": "Limit number of search results to work through."
            },
            "best_practices": "Use crtsh and google sources to discover subdomains and corporate employee email addresses.",
            "pipeline_next": ["Nmap", "Whois"]
        },
        "metagoofil": {
            "name": "Metagoofil Document Metadata Extractor",
            "accepted_inputs": ["Target Domain Name (e.g., kali.org or target.com)"],
            "input_type": "DOMAIN",
            "flags": {
                "-d": "Target domain to search.",
                "-t": "File types to search and download (pdf,doc,xls,ppt,docx,xlsx,ALL).",
                "-l": "Maximum search results limit (Default: 100).",
                "-n": "Maximum files to download per filetype (Default: 100).",
                "-o": "Directory path to save downloaded documents.",
                "-f": "Save HTML links output file name.",
                "-e": "Delay in seconds between search engine queries.",
                "-r": "Number of downloader threads (Default: 8).",
                "-i": "URL request timeout in seconds.",
                "-u": "Custom or randomized User-Agent header.",
                "-w": "Download files locally instead of just viewing search results."
            },
            "best_practices": "Use Metagoofil during OSINT reconnaissance to locate public PDF/DOCX files and extract internal username, software version, and filepath metadata.",
            "pipeline_next": ["theHarvester", "Photon", "Nmap"]
        },
        "amass": {
            "name": "OWASP Amass In-depth DNS & Network Mapper",
            "accepted_inputs": ["Target Domain Name (e.g., example.com)"],
            "input_type": "DOMAIN",
            "flags": {
                "enum": "Subcommand for DNS enumeration and network mapping.",
                "intel": "Subcommand for intelligence gathering (WHOIS, ASN, CIDR).",
                "-d": "Target domain name to scan.",
                "-passive": "Enable passive reconnaissance mode (OSINT scraping only).",
                "-active": "Enable active reconnaissance (zone transfers, cert pulling).",
                "-brute": "Perform subdomain name alterations and brute-forcing.",
                "-ip": "Show resolved IP addresses alongside subdomains.",
                "-src": "Show data source attribution for discovered DNS names.",
                "-w": "Custom wordlist path for subdomain brute forcing.",
                "-o": "Save output results to specified text file."
            },
            "best_practices": "Begin attack surface discovery using passive OSINT mode (`amass enum -passive -d target.com`), then run active mode with IP mapping (`amass enum -active -ip -d target.com`).",
            "pipeline_next": ["Nmap", "Nikto", "Gobuster"]
        },
        "john": {
            "name": "John the Ripper Password Cracker",
            "accepted_inputs": ["Path to text file containing password hashes"],
            "input_type": "HASH_FILE",
            "flags": {
                "--wordlist=": "Specify wordlist dictionary file.",
                "--format=": "Specify hash format (e.g., raw-md5, NT, sha512crypt).",
                "--show": "Display previously cracked passwords."
            },
            "best_practices": "Run HashID first to determine exact hash format string to provide to --format.",
            "pipeline_next": ["AI Copilot"]
        },
        "hashcat": {
            "name": "Hashcat Advanced Password Recovery Engine",
            "accepted_inputs": ["Target Hash File or Hash String (e.g. example500.hash)"],
            "input_type": "HASH_FILE",
            "flags": {
                "-m": "Hash type code (e.g. 0=MD5, 100=SHA1, 500=md5crypt, 1000=NTLM, 1800=SHA512-Unix, 2500=WPA/WPA2).",
                "-a": "Attack mode (0=Straight/Wordlist, 1=Combinator, 3=Brute-force/Mask, 6=Hybrid Wordlist+Mask, 7=Hybrid Mask+Wordlist).",
                "-b": "Run benchmark test on supported hash-modes to measure GPU/CPU hash rate.",
                "-O": "Enable hand-optimized kernel code for max speed (limits max password length to 32).",
                "-r": "Apply rules file to expand wordlist candidate permutations (e.g. rules/best64.rule).",
                "-o": "Specify output text file for recovered cracked plaintexts.",
                "--force": "Ignore OpenCL/GPU driver warnings.",
                "--show": "Compare hash list against potfile and show previously cracked hashes."
            },
            "best_practices": "Identify hash algorithm with HashID first, benchmark your hardware using `hashcat -b`, and use `-O` for maximum GPU cracking throughput.",
            "pipeline_next": ["AI Copilot", "Hydra"]
        },
        "ncrack": {
            "name": "Ncrack High-Speed Network Authentication Cracker",
            "accepted_inputs": ["Target IP (e.g. 192.168.1.100)", "Target Hostname (e.g. scanme.nmap.org)", "Target List File (-iL win.txt)"],
            "input_type": "HOST_OR_NETWORK",
            "flags": {
                "-v": "Enable verbose output mode (shows live connection & cracking status).",
                "-vv": "Enable extra high verbosity mode.",
                "-p": "Specify service list/protocol (e.g. -p rdp, -p ssh, -p ftp:2121, -p smb).",
                "-iL": "Read targets from input list/file (e.g. -iL win.txt).",
                "-iX": "Input targets from Nmap XML scan output file (-oX).",
                "--user": "Single target username to test (e.g. --user victim or --user Administrator).",
                "-U": "Username dictionary wordlist file (e.g. -U users.txt).",
                "--pass": "Single password to test across users (e.g. --pass password123).",
                "-P": "Password dictionary wordlist file (e.g. -P passes.txt).",
                "CL=": "Max connection limit: maximum number of concurrent parallel connections (e.g. CL=1).",
                "cl=": "Min connection limit: minimum number of concurrent parallel connections (e.g. cl=1).",
                "-T<0-5>": "Timing template: 0 (Paranoid), 1 (Sneaky), 2 (Polite), 3 (Normal), 4 (Aggressive), 5 (Insane).",
                "--stealthy-linear": "Try credentials using only one connection per host in a round-robin loop.",
                "--connection-limit": "Set threshold for total concurrent connections across all targets.",
                "ssl": "Enable SSL/TLS encapsulation for specified service."
            },
            "best_practices": "For stable RDP and SMB authentication without causing host connection drops or denial-of-service, set a conservative connection limit like `CL=1` or `CL=4` and use verbose mode (`-v`).",
            "pipeline_next": ["Hydra", "John the Ripper", "AI Copilot"]
        },
    }

    @classmethod
    def validate_input(cls, tool_key: str, user_input: str) -> Tuple[bool, str, str]:
        """
        Validates target input syntax against the tool's requirements.
        Returns: (is_valid: bool, status_badge: str, message: str)
        """
        raw = user_input.strip()
        if not raw:
            return False, "EMPTY", "Please enter a target address to begin."

        tool = cls.TOOL_SCHEMAS.get(tool_key.lower())
        if not tool:
            return True, "READY", "Input format check passed."

        itype = tool["input_type"]

        if itype == "URL":
            if cls.URL_REGEX.match(raw):
                return True, "VALID_URL", "Valid web URL format."
            return False, "INVALID_FORMAT", "Tool requires a valid HTTP/HTTPS URL (e.g., http://target.com)."

        elif itype == "URL_WITH_PARAM":
            if cls.URL_REGEX.match(raw):
                if "?" in raw and "=" in raw:
                    return True, "VALID_PARAM_URL", "Valid parameterized URL ready for SQL injection testing."
                return True, "WARNING_NO_PARAM", "URL lacks query parameters (e.g. ?id=1). Testing might require --forms or POST data."
            return False, "INVALID_FORMAT", "Please provide a valid URL (e.g., http://target.com/page.php?id=1)."

        elif itype == "URL_OR_HOST":
            if cls.URL_REGEX.match(raw) or cls.IP_REGEX.match(raw) or cls.DOMAIN_REGEX.match(raw):
                return True, "VALID_TARGET", "Valid host or URL format."
            return False, "INVALID_FORMAT", "Please provide a valid URL, IP address, or domain name."

        elif itype == "HOST_OR_NETWORK":
            if cls.IP_REGEX.match(raw) or cls.CIDR_REGEX.match(raw) or cls.DOMAIN_REGEX.match(raw):
                return True, "VALID_HOST", "Valid host IP, CIDR subnet, or domain."
            if raw.startswith("http://") or raw.startswith("https://"):
                clean = re.sub(r"^https?://", "", raw).split("/")[0]
                return True, "URL_CONVERTIBLE", f"Converted web URL to clean hostname: '{clean}'."
            return False, "INVALID_FORMAT", "Enter an IP address (192.168.1.1), CIDR (10.0.0.0/24), or domain (target.com)."

        elif itype == "DOMAIN":
            if cls.DOMAIN_REGEX.match(raw):
                return True, "VALID_DOMAIN", "Valid domain name format."
            clean = re.sub(r"^https?://", "", raw).split("/")[0]
            if cls.DOMAIN_REGEX.match(clean):
                return True, "VALID_DOMAIN", f"Domain extracted: '{clean}'."
            return False, "INVALID_FORMAT", "Please enter a clean domain name without protocol (e.g., example.com)."

        elif itype == "DOMAIN_OR_IP":
            if cls.DOMAIN_REGEX.match(raw) or cls.IP_REGEX.match(raw):
                return True, "VALID_TARGET", "Valid domain or IP address."
            return False, "INVALID_FORMAT", "Please enter a domain name or IP address."

        return True, "READY", "Input format accepted."

    @classmethod
    def get_tool_guide(cls, tool_key: str) -> Dict[str, Any]:
        """Returns comprehensive guidance and flag catalog for a tool."""
        return cls.TOOL_SCHEMAS.get(tool_key.lower(), {
            "name": tool_key.capitalize(),
            "accepted_inputs": ["Target IP or Domain"],
            "flags": {},
            "best_practices": "Ensure authorized testing scope before running.",
            "pipeline_next": []
        })
