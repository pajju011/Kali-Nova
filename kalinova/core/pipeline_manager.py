"""
Inter-Tool Pipeline Manager for Kali-Nova.
Parses live tool stdout, extracts security artifacts (IPs, URLs, endpoints, hashes),
and bridges data flow between consecutive security tools.
"""

import re
from typing import Dict, Any, List, Optional
from core.app_state import app_state


class PipelineManager:
    """
    Manages automated data handoff from one security tool to another.
    Extracts discovered artifacts from raw tool outputs and prepares
    input contexts for subsequent tools.
    """

    # Regex extractors
    URL_EXTRACTOR = re.compile(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*", re.IGNORECASE)
    SUBDOMAIN_EXTRACTOR = re.compile(r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b")
    ENDPOINT_EXTRACTOR = re.compile(r"(?:Found|Directory|Path|URI):\s*([/\w\.-]+(?:\?[\w=&%-]+)?)", re.IGNORECASE)
    PARAM_URL_EXTRACTOR = re.compile(r"https?://[^\s]+\?[^\s=&]+=[^\s&]+", re.IGNORECASE)
    HASH_MD5_EXTRACTOR = re.compile(r"\b[a-fA-F0-9]{32}\b")
    HASH_SHA256_EXTRACTOR = re.compile(r"\b[a-fA-F0-9]{64}\b")
    EMAIL_EXTRACTOR = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")

    @classmethod
    def ingest_output(cls, tool_name: str, raw_output: str, target: Optional[str] = None):
        """
        Parses raw tool stdout stream and registers extracted artifacts into AppState.
        """
        tool_lower = (tool_name or "").lower()

        if target:
            app_state.add_pipeline_artifact("targets", target)

        # 1. Extract Web URLs
        found_urls = cls.URL_EXTRACTOR.findall(raw_output)
        for url in found_urls:
            app_state.add_pipeline_artifact("web_urls", url.rstrip(".,;)\"\'"))

        # 2. Extract Parameterized URLs for Sqlmap
        param_urls = cls.PARAM_URL_EXTRACTOR.findall(raw_output)
        for purl in param_urls:
            app_state.add_pipeline_artifact("fuzzed_endpoints", purl.rstrip(".,;)\"\'"))

        # 3. Extract Fuzzed Endpoints (Gobuster / Nikto)
        if "gobuster" in tool_lower or "nikto" in tool_lower:
            # Look for line patterns like /admin (Status: 200) or + /index.php
            lines = raw_output.splitlines()
            for line in lines:
                line_str = line.strip()
                if line_str.startswith("/") or "+ /" in line_str:
                    parts = line_str.split()
                    for p in parts:
                        if p.startswith("/"):
                            app_state.add_pipeline_artifact("fuzzed_endpoints", p)

        # 4. Extract Discovered Subdomains & Emails (theHarvester / Whois / Metagoofil / Amass)
        if "theharvester" in tool_lower or "whois" in tool_lower or "metagoofil" in tool_lower or "amass" in tool_lower or "recon" in tool_lower:
            emails = cls.EMAIL_EXTRACTOR.findall(raw_output)
            for em in emails:
                app_state.add_pipeline_artifact("emails", em)

        # 5. Extract Hashes (Sqlmap / Hydra / John)
        if "sqlmap" in tool_lower or "dump" in raw_output.lower():
            md5s = cls.HASH_MD5_EXTRACTOR.findall(raw_output)
            for h in md5s[:5]:
                app_state.add_pipeline_artifact("hashes", h)

        # 6. Synthesize Web URLs from Open Ports if Nmap finished
        if "nmap" in tool_lower and target:
            clean_host = re.sub(r"^https?://", "", target).split("/")[0]
            for p in app_state.open_ports:
                if p in [80, 8080, 8000, 8888, 9000]:
                    scheme = "http"
                    url = f"{scheme}://{clean_host}:{p}" if p != 80 else f"{scheme}://{clean_host}"
                    app_state.add_pipeline_artifact("web_urls", url)
                elif p in [443, 8443, 9443]:
                    scheme = "https"
                    url = f"{scheme}://{clean_host}:{p}" if p != 443 else f"{scheme}://{clean_host}"
                    app_state.add_pipeline_artifact("web_urls", url)

    @classmethod
    def get_best_target_for_tool(cls, target_tool: str) -> Optional[str]:
        """
        Retrieves the most suitable target parameter for a given tool from the pipeline state.
        """
        tool = target_tool.lower()
        artifacts = app_state.pipeline_artifacts

        # Web Vulnerability Scanners (Nikto, Gobuster) prefer base URLs
        if tool in ["nikto", "gobuster", "whatweb", "wfuzz"]:
            if artifacts["web_urls"]:
                return artifacts["web_urls"][0]
            if artifacts["targets"]:
                t = artifacts["targets"][0]
                return t if t.startswith("http") else f"http://{t}"

        # SQL Injection Scanner (Sqlmap) prefers endpoints with parameters
        elif tool == "sqlmap":
            if artifacts["fuzzed_endpoints"]:
                for ep in artifacts["fuzzed_endpoints"]:
                    if ep.startswith("http") and "?" in ep:
                        return ep
                # Combine base url + endpoint
                if artifacts["web_urls"] and artifacts["fuzzed_endpoints"]:
                    base = artifacts["web_urls"][0].rstrip("/")
                    ep = artifacts["fuzzed_endpoints"][0]
                    if not ep.startswith("/"):
                        ep = f"/{ep}"
                    return f"{base}{ep}"
            if artifacts["web_urls"]:
                return artifacts["web_urls"][0]
            if artifacts["targets"]:
                return artifacts["targets"][0]

        # Password / Service Crackers (Hydra, Netcat, SSLScan) prefer Host/IP
        elif tool in ["hydra", "nmap", "sslscan", "sslyze", "netcat"]:
            if artifacts["targets"]:
                t = artifacts["targets"][0]
                # Strip http:// scheme if present
                return re.sub(r"^https?://", "", t).split("/")[0]

        # Hash Crackers (John, Hashcat) prefer discovered hashes
        elif tool in ["john", "hashcat"]:
            if artifacts["hashes"]:
                return artifacts["hashes"][0]

        # Recon Tools (Whois, theHarvester, Metagoofil, Amass) prefer Domain
        elif tool in ["whois", "theharvester", "metagoofil", "amass"]:
            if artifacts["subdomains"]:
                return artifacts["subdomains"][0]
            if artifacts["targets"]:
                return re.sub(r"^https?://", "", artifacts["targets"][0]).split("/")[0]

        # Fallback to general target if present
        if artifacts["targets"]:
            return artifacts["targets"][0]

        return None
