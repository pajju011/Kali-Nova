"""
ToolRegistry — Dynamic registry of all available tools.

Manages tool metadata, type declarations, parser mappings,
and availability detection. Designed to scale from 4 MVP
tools to 600+ via plugin-based addition.
"""

import logging
import shutil
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Type

logger = logging.getLogger(__name__)


@dataclass
class ToolInfo:
    """Metadata for a registered tool."""
    name: str
    display_name: str
    description: str
    tool_type: str  # "assessment", "action", "utility"
    category: str  # Kali category e.g. "information_gathering"
    cli_binary: str  # Binary name e.g. "nmap"
    ml_enabled: bool = False
    report_enabled: bool = False
    icon_name: str = ""
    is_available: bool = False
    binary_path: str = ""
    options: list = field(default_factory=list)


# ---------- Built-in tool definitions (MVP) ----------

_BUILTIN_TOOLS: Dict[str, ToolInfo] = {
    "nmap": ToolInfo(
        name="nmap",
        display_name="Nmap",
        description=(
            "Network exploration and security auditing tool. "
            "Discovers hosts, open ports, running services, and OS details on a network."
        ),
        tool_type="assessment",
        category="information_gathering",
        cli_binary="nmap",
        ml_enabled=True,
        report_enabled=True,
        icon_name="nmap",
    ),
    "nikto": ToolInfo(
        name="nikto",
        display_name="Nikto",
        description=(
            "Web server vulnerability scanner. "
            "Checks for dangerous files, outdated server software, and common misconfigurations."
        ),
        tool_type="assessment",
        category="vulnerability_analysis",
        cli_binary="nikto",
        ml_enabled=True,
        report_enabled=True,
        icon_name="nikto",
    ),
    "john": ToolInfo(
        name="john",
        display_name="John the Ripper",
        description=(
            "Password hash cracker. "
            "Detects hash types and cracks password hashes using wordlists or brute-force."
        ),
        tool_type="action",
        category="password_attacks",
        cli_binary="john",
        ml_enabled=False,
        report_enabled=False,
        icon_name="john",
    ),
    "hydra": ToolInfo(
        name="hydra",
        display_name="Hydra",
        description=(
            "Fast online password brute-forcer. "
            "Supports SSH, FTP, HTTP, and 50+ other protocols for login testing."
        ),
        tool_type="action",
        category="password_attacks",
        cli_binary="hydra",
        ml_enabled=False,
        report_enabled=False,
        icon_name="hydra",
    ),
}

# Kali Linux tool categories
KALI_CATEGORIES = {
    "information_gathering": "Information Gathering",
    "vulnerability_analysis": "Vulnerability Analysis",
    "web_applications": "Web Applications",
    "password_attacks": "Password Attacks",
    "wireless_attacks": "Wireless Attacks",
    "exploitation_tools": "Exploitation Tools",
    "sniffing_spoofing": "Sniffing & Spoofing",
    "post_exploitation": "Post-Exploitation",
    "forensics": "Forensics",
    "reporting_tools": "Reporting Tools",
    "social_engineering": "Social Engineering",
    "reverse_engineering": "Reverse Engineering",
    "hardware_hacking": "Hardware Hacking",
    "maintaining_access": "Maintaining Access",
}


class ToolRegistry:
    """
    Central registry for all Kalinova tools.

    Manages tool registration, availability detection,
    and lookup. Supports both built-in and plugin-based tools.
    """

    def __init__(self):
        self._tools: Dict[str, ToolInfo] = {}
        self._load_builtin_tools()

    def _load_builtin_tools(self) -> None:
        """Load built-in MVP tool definitions."""
        for name, tool_info in _BUILTIN_TOOLS.items():
            self.register(tool_info)
        logger.info(f"Loaded {len(_BUILTIN_TOOLS)} built-in tools.")

    def register(self, tool_info: ToolInfo) -> None:
        """
        Register a tool in the registry.

        Args:
            tool_info: ToolInfo dataclass with tool metadata.
        """
        # Check binary availability
        binary_path = shutil.which(tool_info.cli_binary)
        tool_info.is_available = binary_path is not None
        tool_info.binary_path = binary_path or ""

        self._tools[tool_info.name] = tool_info

        status = "available" if tool_info.is_available else "NOT FOUND"
        logger.info(
            f"Registered tool: {tool_info.display_name} "
            f"[{tool_info.tool_type}] — {status}"
        )

    def get(self, name: str) -> Optional[ToolInfo]:
        """Get tool info by name."""
        return self._tools.get(name)

    def get_all(self) -> List[ToolInfo]:
        """Get all registered tools."""
        return list(self._tools.values())

    def get_available(self) -> List[ToolInfo]:
        """Get only tools that are installed on the system."""
        return [t for t in self._tools.values() if t.is_available]

    def get_by_type(self, tool_type: str) -> List[ToolInfo]:
        """Get tools filtered by type (assessment/action/utility)."""
        return [t for t in self._tools.values() if t.tool_type == tool_type]

    def get_by_category(self, category: str) -> List[ToolInfo]:
        """Get tools filtered by Kali category."""
        return [t for t in self._tools.values() if t.category == category]

    def get_categories_with_tools(self) -> Dict[str, List[ToolInfo]]:
        """Get a mapping of categories to their tools."""
        categories: Dict[str, List[ToolInfo]] = {}
        for tool in self._tools.values():
            cat = tool.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(tool)
        return categories

    def is_registered(self, name: str) -> bool:
        """Check if a tool is registered."""
        return name in self._tools

    def is_available(self, name: str) -> bool:
        """Check if a tool is registered AND installed."""
        tool = self._tools.get(name)
        return tool.is_available if tool else False

    def refresh_availability(self) -> None:
        """Re-check binary availability for all tools."""
        for tool in self._tools.values():
            binary_path = shutil.which(tool.cli_binary)
            tool.is_available = binary_path is not None
            tool.binary_path = binary_path or ""

    @property
    def tool_count(self) -> int:
        """Total number of registered tools."""
        return len(self._tools)

    @property
    def available_count(self) -> int:
        """Number of tools actually available on the system."""
        return len(self.get_available())
