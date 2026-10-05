"""
Synthetic Dataset Generator for Penetration Testing Scenario Transitions.
Generates 5,000+ realistic PTES / MITRE ATT&CK workflow samples for ML model training.
"""

import json
import random
from typing import List, Dict, Any


def generate_synthetic_scenarios(count: int = 5000) -> List[Dict[str, Any]]:
    """
    Generates realistic penetration testing state transitions.
    Each sample contains:
      - open_ports: list of int
      - events: list of str
      - last_tool: str
      - risk_score: int
      - global_risk: str
      - has_web_urls: bool
      - has_fuzzed_endpoints: bool
      - has_hashes: bool
      - target_action: str (Ground Truth Label)
    """
    samples = []

    for _ in range(count):
        scenario_type = random.choice([
            "RECON_INIT",
            "RECON_COMPLETE",
            "WEB_DISCOVERED",
            "WEB_FUZZED",
            "SQLI_DETECTED",
            "SSH_EXPOSED",
            "FTP_EXPOSED",
            "SSL_AUDIT_NEEDED",
            "HASH_CAPTURED",
            "CRITICAL_REMEDIATION",
            "GENERAL_NETWORK"
        ])

        open_ports = []
        events = []
        last_tool = "none"
        risk_score = 0
        global_risk = "LOW"
        has_web_urls = False
        has_fuzzed_endpoints = False
        has_hashes = False
        target_action = "nmap"

        if scenario_type == "RECON_INIT":
            # Initial engagement: no scan executed yet or domain provided
            last_tool = random.choice(["none", "whois"])
            target_action = random.choice(["whois", "theharvester", "nmap"])
            risk_score = random.randint(0, 2)
            global_risk = "LOW"

        elif scenario_type == "RECON_COMPLETE":
            # theHarvester or Whois finished, subdomains / emails found
            last_tool = random.choice(["theharvester", "whois"])
            events = random.sample(["EMAIL_ENUM", "SUBDOMAIN_ENUM"], random.randint(1, 2))
            risk_score = random.randint(2, 4)
            global_risk = "LOW"
            target_action = "nmap"  # Next logical step is port scan

        elif scenario_type == "WEB_DISCOVERED":
            # Nmap completed, found web ports 80/443/8080
            last_tool = "nmap"
            open_ports = random.choice([
                [80], [443], [80, 443], [80, 8080], [8080], [80, 443, 8443]
            ])
            has_web_urls = True
            risk_score = random.randint(2, 5)
            global_risk = "LOW" if risk_score <= 3 else "MEDIUM"
            target_action = random.choice(["nikto", "gobuster"])

        elif scenario_type == "WEB_FUZZED":
            # Gobuster / Nikto ran, directories discovered
            last_tool = random.choice(["gobuster", "nikto"])
            open_ports = [80, 443] if random.random() > 0.3 else [8080]
            events = ["DIR_ENUM"]
            has_web_urls = True
            has_fuzzed_endpoints = True
            risk_score = random.randint(4, 7)
            global_risk = "MEDIUM"
            # Next step is to test endpoints for SQLi or Nikto
            target_action = "sqlmap" if random.random() > 0.4 else "nikto"

        elif scenario_type == "SQLI_DETECTED":
            # SQL Injection indicator found
            last_tool = random.choice(["nikto", "gobuster", "sqlmap"])
            open_ports = [80] if random.random() > 0.5 else [80, 443]
            events = ["SQL_INJECTION"]
            if random.random() > 0.5:
                events.append("DIR_ENUM")
            has_web_urls = True
            has_fuzzed_endpoints = True
            risk_score = random.randint(8, 14)
            global_risk = "HIGH"
            target_action = "sqlmap"

        elif scenario_type == "SSH_EXPOSED":
            # SSH port 22 exposed, maybe brute force detected
            last_tool = "nmap"
            open_ports = [22] if random.random() > 0.4 else [22, 80]
            if random.random() > 0.5:
                events.append("BRUTE_FORCE")
                risk_score = random.randint(6, 9)
                global_risk = "MEDIUM"
            else:
                risk_score = random.randint(2, 4)
                global_risk = "LOW"
            target_action = "hydra"

        elif scenario_type == "FTP_EXPOSED":
            last_tool = "nmap"
            open_ports = [21]
            risk_score = random.randint(3, 6)
            global_risk = "MEDIUM"
            target_action = "hydra"

        elif scenario_type == "SSL_AUDIT_NEEDED":
            last_tool = "nmap"
            open_ports = [443] if random.random() > 0.5 else [443, 8443]
            has_web_urls = True
            events = ["SSL_WEAKNESS"] if random.random() > 0.5 else []
            risk_score = random.randint(2, 5)
            global_risk = "LOW" if risk_score <= 3 else "MEDIUM"
            target_action = "sslscan"

        elif scenario_type == "HASH_CAPTURED":
            last_tool = "sqlmap"
            events = ["SQL_INJECTION", "SECRET_LEAK"]
            has_hashes = True
            risk_score = random.randint(10, 16)
            global_risk = "HIGH"
            target_action = "john"

        elif scenario_type == "CRITICAL_REMEDIATION":
            last_tool = random.choice(["sqlmap", "hydra", "john"])
            events = random.sample(["SQL_INJECTION", "SECRET_LEAK", "BRUTE_FORCE"], random.randint(2, 3))
            risk_score = random.randint(14, 20)
            global_risk = "HIGH"
            has_hashes = True
            target_action = "remediate"

        elif scenario_type == "GENERAL_NETWORK":
            last_tool = random.choice(["none", "nmap"])
            open_ports = random.sample([21, 22, 80, 443, 445, 3306, 3389, 8080], random.randint(1, 4))
            risk_score = random.randint(2, 8)
            global_risk = "LOW" if risk_score <= 3 else "MEDIUM"
            target_action = "nmap" if not open_ports else "nikto"

        samples.append({
            "open_ports": open_ports,
            "events": events,
            "last_tool": last_tool,
            "risk_score": risk_score,
            "global_risk": global_risk,
            "has_web_urls": has_web_urls,
            "has_fuzzed_endpoints": has_fuzzed_endpoints,
            "has_hashes": has_hashes,
            "target_action": target_action
        })

    return samples


if __name__ == "__main__":
    data = generate_synthetic_scenarios(5000)
    with open("scenario_dataset.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"Generated {len(data)} synthetic pentest scenarios.")
