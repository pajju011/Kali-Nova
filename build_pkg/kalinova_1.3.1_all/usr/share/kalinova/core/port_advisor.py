"""
Port Prioritization & Strategy Advisor for Kali-Nova.
Provides categorized port scanning profiles, risk severity ratings, and target intelligence.
"""

from typing import Dict, List, Any


class PortAdvisor:
    """
    Intelligent Port Advisor that recommends optimal port scanning profiles
    and provides contextual explanations on why specific ports are high priority.
    """

    PORT_PROFILES: Dict[str, Dict[str, Any]] = {
        "FAST_TRIAGE": {
            "name": "⚡ Fast Triage (Top 20 Ports)",
            "description": "Scans the top 20 most frequently targeted ports. Completes in under 10 seconds and identifies 85%+ of exposed attack surfaces.",
            "ports": [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 1433, 1521, 3306, 3389, 5432, 5900, 8000, 8080, 8443, 8888],
            "recommended_tools": ["Nmap", "Nikto", "Hydra"],
            "rationale": "High-efficiency initial sweep to detect active web services, databases, and remote management ports before deep enumeration."
        },
        "WEB_SERVICES": {
            "name": "🌐 Web Infrastructure & APIs",
            "description": "Targets HTTP, HTTPS, alternative web ports, development servers, and REST/GraphQL API gateways.",
            "ports": [80, 443, 8000, 8008, 8080, 8081, 8443, 8888, 9000, 9090, 9443],
            "recommended_tools": ["Nikto", "Gobuster", "WhatWeb", "Wfuzz", "Sqlmap"],
            "rationale": "Web applications account for the majority of initial breach vectors (OWASP Top 10 vulnerabilities, directory leaks, SQLi)."
        },
        "ACTIVE_DIRECTORY": {
            "name": "🏢 Network & Active Directory",
            "description": "Essential ports for internal network assessments, domain controllers, SMB file shares, and RPC services.",
            "ports": [53, 88, 135, 139, 389, 445, 464, 593, 636, 3268, 3269, 3389, 5985, 5986],
            "recommended_tools": ["Nmap", "Hydra", "Netcat"],
            "rationale": "Critical for detecting Kerberoasting opportunities, SMB signing misconfigurations, and lateral movement paths."
        },
        "DATABASES": {
            "name": "🗄️ Database & Cache Tier",
            "description": "Probes relational databases, NoSQL stores, and memory caching services.",
            "ports": [1433, 1521, 3306, 5432, 5984, 6379, 7000, 9042, 9200, 9300, 11211, 27017, 27018],
            "recommended_tools": ["Nmap", "Sqlmap", "Hydra"],
            "rationale": "Exposed database instances frequently have default credentials or lack network isolation, leading to direct data exfiltration."
        },
        "REMOTE_ACCESS": {
            "name": "🔑 Remote Management & Shells",
            "description": "Identifies SSH, Telnet, RDP, VNC, and remote administrative interfaces.",
            "ports": [21, 22, 23, 3389, 5900, 5901, 5985, 5986],
            "recommended_tools": ["Hydra", "Nmap", "Netcat"],
            "rationale": "High priority for brute-force vulnerability checks and credential stuffing resilience testing."
        },
        "FULL_AUDIT": {
            "name": "🔍 Comprehensive Perimeter Sweep",
            "description": "Scans all 65,535 TCP ports to discover non-standard listeners and hidden administrative backdoors.",
            "ports": [],  # Represents 1-65535
            "port_string": "1-65535",
            "recommended_tools": ["Nmap"],
            "rationale": "Exhaustive testing required for compliance and perimeter hardening, discovering services obfuscated on custom ports."
        }
    }

    PORT_DETAILS: Dict[int, Dict[str, Any]] = {
        21: {"service": "FTP", "risk": "HIGH", "vuln": "Cleartext credentials, anonymous login", "next_tool": "Hydra"},
        22: {"service": "SSH", "risk": "MEDIUM", "vuln": "Weak key/password authentication, brute force", "next_tool": "Hydra"},
        23: {"service": "Telnet", "risk": "CRITICAL", "vuln": "Unencrypted communication stream", "next_tool": "Netcat"},
        25: {"service": "SMTP", "risk": "MEDIUM", "vuln": "Open mail relay, user enumeration", "next_tool": "Nmap"},
        53: {"service": "DNS", "risk": "MEDIUM", "vuln": "Zone transfer (AXFR), DNS cache poisoning", "next_tool": "theHarvester"},
        80: {"service": "HTTP", "risk": "HIGH", "vuln": "OWASP Top 10, Web directory exposure, SQLi", "next_tool": "Nikto"},
        139: {"service": "NetBIOS", "risk": "HIGH", "vuln": "Information disclosure, null session enumeration", "next_tool": "Nmap"},
        443: {"service": "HTTPS", "risk": "MEDIUM", "vuln": "TLS/SSL cipher weaknesses, web vulnerabilities", "next_tool": "SSLScan"},
        445: {"service": "SMB", "risk": "CRITICAL", "vuln": "EternalBlue, SMB relay, unauthenticated shares", "next_tool": "Nmap"},
        1433: {"service": "MSSQL", "risk": "HIGH", "vuln": "xp_cmdshell command execution, weak sa password", "next_tool": "Sqlmap"},
        3306: {"service": "MySQL", "risk": "HIGH", "vuln": "Default root with empty password, remote access", "next_tool": "Sqlmap"},
        3389: {"service": "RDP", "risk": "HIGH", "vuln": "BlueKeep vulnerability, credential brute force", "next_tool": "Hydra"},
        5432: {"service": "PostgreSQL", "risk": "HIGH", "vuln": "Database injection, weak authentication", "next_tool": "Sqlmap"},
        6379: {"service": "Redis", "risk": "CRITICAL", "vuln": "Unauthenticated access, arbitrary file write / SSH key injection", "next_tool": "Netcat"},
        8080: {"service": "HTTP-Proxy / Dev Web", "risk": "HIGH", "vuln": "Unprotected admin consoles (Tomcat, Jenkins)", "next_tool": "Nikto"},
        8443: {"service": "HTTPS-Alt", "risk": "MEDIUM", "vuln": "Administrative portals, self-signed certificates", "next_tool": "Nikto"},
        27017: {"service": "MongoDB", "risk": "CRITICAL", "vuln": "No authentication enabled by default in legacy setups", "next_tool": "Nmap"},
    }

    @classmethod
    def get_profile(cls, profile_key: str) -> Dict[str, Any]:
        """Retrieve full profile metadata by key."""
        return cls.PORT_PROFILES.get(profile_key, cls.PORT_PROFILES["FAST_TRIAGE"])

    @classmethod
    def get_ports_string(cls, profile_key: str) -> str:
        """Format ports for CLI execution (e.g. '80,443,8080' or '1-65535')."""
        prof = cls.get_profile(profile_key)
        if "port_string" in prof:
            return prof["port_string"]
        return ",".join(str(p) for p in prof.get("ports", []))

    @classmethod
    def analyze_ports(cls, open_ports: List[int]) -> List[Dict[str, Any]]:
        """
        Analyze a list of discovered open ports and return risk metadata and recommended next steps.
        """
        findings = []
        for port in open_ports:
            if port in cls.PORT_DETAILS:
                info = cls.PORT_DETAILS[port]
                findings.append({
                    "port": port,
                    "service": info["service"],
                    "risk": info["risk"],
                    "vulnerability": info["vuln"],
                    "recommended_tool": info["next_tool"]
                })
            else:
                findings.append({
                    "port": port,
                    "service": f"Custom Service (Port {port})",
                    "risk": "MEDIUM",
                    "vulnerability": "Unidentified network listener",
                    "recommended_tool": "Nmap"
                })
        return findings
