"""
FeatureExtractor — Converts parsed scan results to ML feature vectors.

Extracts numeric features from Nmap and Nikto parsed data
for input to the next-tool prediction model.
"""

import logging
from typing import Dict

logger = logging.getLogger(__name__)


class FeatureExtractor:
    """
    Extracts numeric feature vectors from parsed tool output.

    Each tool type has a dedicated extraction method that
    produces a consistent feature dictionary for the ML model.
    """

    def extract(self, tool_name: str, parsed_data: dict) -> Dict[str, float]:
        """
        Extract feature vector from parsed tool output.

        Args:
            tool_name: Name of the tool (e.g., "nmap", "nikto").
            parsed_data: Structured dictionary from parser.

        Returns:
            Dictionary of feature_name → numeric_value.
        """
        extractors = {
            "nmap": self._extract_nmap_features,
            "nikto": self._extract_nikto_features,
        }

        extractor = extractors.get(tool_name.lower())
        if extractor is None:
            logger.warning(f"No feature extractor for tool: {tool_name}")
            return {}

        features = extractor(parsed_data)
        logger.info(f"Extracted {len(features)} features from {tool_name}")
        return features

    def _extract_nmap_features(self, data: dict) -> Dict[str, float]:
        """Extract features from Nmap parsed results."""
        features = {
            "open_ports": 0.0,
            "closed_ports": 0.0,
            "filtered_ports": 0.0,
            "http_detected": 0.0,
            "https_detected": 0.0,
            "ssh_detected": 0.0,
            "ftp_detected": 0.0,
            "smb_detected": 0.0,
            "rdp_detected": 0.0,
            "dns_detected": 0.0,
            "telnet_detected": 0.0,
            "mysql_detected": 0.0,
            "total_services": 0.0,
            "has_web_server": 0.0,
            "has_auth_service": 0.0,
        }

        features["open_ports"] = float(data.get("open_ports", 0))
        features["closed_ports"] = float(data.get("closed_ports", 0))
        features["filtered_ports"] = float(data.get("filtered_ports", 0))

        # Scan all hosts and ports for service detection
        services_found = set()
        for host in data.get("hosts", []):
            for port in host.get("ports", []):
                if port.get("state") != "open":
                    continue

                service = port.get("service", "").lower()
                port_num = port.get("port", 0)
                services_found.add(service)

                # Service-specific detection
                if service in ("http", "http-proxy") or port_num in (80, 8080, 8000):
                    features["http_detected"] = 1.0
                if service in ("https", "ssl/http") or port_num in (443, 8443):
                    features["https_detected"] = 1.0
                if service == "ssh" or port_num == 22:
                    features["ssh_detected"] = 1.0
                if service == "ftp" or port_num == 21:
                    features["ftp_detected"] = 1.0
                if service in ("microsoft-ds", "netbios-ssn", "smb") or port_num in (445, 139):
                    features["smb_detected"] = 1.0
                if service in ("ms-wbt-server", "rdp") or port_num == 3389:
                    features["rdp_detected"] = 1.0
                if service == "domain" or port_num == 53:
                    features["dns_detected"] = 1.0
                if service == "telnet" or port_num == 23:
                    features["telnet_detected"] = 1.0
                if service == "mysql" or port_num == 3306:
                    features["mysql_detected"] = 1.0

        features["total_services"] = float(len(services_found))
        features["has_web_server"] = 1.0 if (
            features["http_detected"] or features["https_detected"]
        ) else 0.0
        features["has_auth_service"] = 1.0 if (
            features["ssh_detected"] or features["ftp_detected"] or
            features["rdp_detected"] or features["telnet_detected"]
        ) else 0.0

        return features

    def _extract_nikto_features(self, data: dict) -> Dict[str, float]:
        """Extract features from Nikto parsed results."""
        vulns = data.get("vulnerabilities", [])

        features = {
            "total_vulns": float(len(vulns)),
            "high_severity_count": 0.0,
            "medium_severity_count": 0.0,
            "low_severity_count": 0.0,
            "has_directory_listing": 0.0,
            "has_default_files": 0.0,
            "has_outdated_server": 0.0,
            "has_misconfig": 0.0,
            "server_type": 0.0,  # Apache=1, Nginx=2, IIS=3, Other=0
        }

        # Classify vulnerabilities by looking at descriptions
        for vuln in vulns:
            desc = vuln.get("description", "").lower()

            # Severity counting (based on keyword analysis)
            if any(kw in desc for kw in [
                "sql injection", "xss", "remote code", "backdoor",
                "command injection", "file inclusion"
            ]):
                features["high_severity_count"] += 1.0
            elif any(kw in desc for kw in [
                "directory listing", "directory indexing",
                "information disclosure", "server version", "outdated"
            ]):
                features["medium_severity_count"] += 1.0
            else:
                features["low_severity_count"] += 1.0

            # Specific detections
            if "directory listing" in desc or "directory indexing" in desc:
                features["has_directory_listing"] = 1.0
            if "default" in desc and ("file" in desc or "page" in desc):
                features["has_default_files"] = 1.0
            if "outdated" in desc or "old version" in desc:
                features["has_outdated_server"] = 1.0
            if "misconfigur" in desc:
                features["has_misconfig"] = 1.0

        # Server type encoding
        server = data.get("server", "").lower()
        if "apache" in server:
            features["server_type"] = 1.0
        elif "nginx" in server:
            features["server_type"] = 2.0
        elif "iis" in server:
            features["server_type"] = 3.0

        return features
