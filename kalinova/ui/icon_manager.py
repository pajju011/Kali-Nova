"""
Icon Manager for Kali-Nova.
Generates and manages professional vector SVG icons for all security tools.
Replaces generic emojis with sleek, dark-mode vector iconography.
"""

import os
from pathlib import Path
from typing import Dict

def get_icons_dir() -> Path:
    """Returns absolute path to resources/icons directory."""
    base_dir = Path(__file__).parent.parent / "resources" / "icons"
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir

TOOL_SVG_MAP: Dict[str, str] = {
    "nmap": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <circle cx="32" cy="32" r="28" fill="#0f172a" stroke="#38bdf8" stroke-width="2.5"/>
  <circle cx="32" cy="32" r="20" fill="none" stroke="#0284c7" stroke-width="1.5" stroke-dasharray="4,3"/>
  <circle cx="32" cy="32" r="12" fill="none" stroke="#0369a1" stroke-width="1.5"/>
  <circle cx="32" cy="32" r="3" fill="#38bdf8"/>
  <line x1="32" y1="4" x2="32" y2="60" stroke="#38bdf8" stroke-width="1.5" stroke-opacity="0.6"/>
  <line x1="4" y1="32" x2="60" y2="32" stroke="#38bdf8" stroke-width="1.5" stroke-opacity="0.6"/>
  <polygon points="32,32 54,16 50,32" fill="#38bdf8" fill-opacity="0.35"/>
  <circle cx="46" cy="18" r="3.5" fill="#f43f5e"/>
</svg>""",

    "whois": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <circle cx="32" cy="32" r="28" fill="#0f172a" stroke="#818cf8" stroke-width="2.5"/>
  <ellipse cx="32" cy="32" rx="14" ry="28" fill="none" stroke="#6366f1" stroke-width="1.8"/>
  <line x1="4" y1="32" x2="60" y2="32" stroke="#6366f1" stroke-width="1.8"/>
  <line x1="10" y1="18" x2="54" y2="18" stroke="#818cf8" stroke-width="1.2" stroke-opacity="0.7"/>
  <line x1="10" y1="46" x2="54" y2="46" stroke="#818cf8" stroke-width="1.2" stroke-opacity="0.7"/>
  <circle cx="44" cy="22" r="4" fill="#a78bfa"/>
  <path d="M44 26 L44 38 L54 38" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round"/>
</svg>""",

    "harvester": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <polygon points="6,10 58,10 40,34 40,54 24,58 24,34" fill="#0f172a" stroke="#f59e0b" stroke-width="2.5" stroke-linejoin="round"/>
  <circle cx="20" cy="18" r="3" fill="#fbbf24"/>
  <circle cx="32" cy="22" r="3" fill="#38bdf8"/>
  <circle cx="44" cy="18" r="3" fill="#f43f5e"/>
  <line x1="12" y1="10" x2="52" y2="10" stroke="#f59e0b" stroke-width="2.5"/>
  <circle cx="32" cy="46" r="4" fill="#f59e0b"/>
</svg>""",

    "metagoofil": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect x="12" y="14" width="32" height="42" rx="4" fill="#0f172a" stroke="#34d399" stroke-width="2.5"/>
  <rect x="20" y="8" width="32" height="42" rx="4" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
  <line x1="26" y1="18" x2="44" y2="18" stroke="#34d399" stroke-width="2" stroke-linecap="round"/>
  <line x1="26" y1="26" x2="40" y2="26" stroke="#34d399" stroke-width="2" stroke-linecap="round"/>
  <line x1="26" y1="34" x2="44" y2="34" stroke="#34d399" stroke-width="2" stroke-linecap="round"/>
  <circle cx="42" cy="40" r="8" fill="#0f172a" stroke="#fbbf24" stroke-width="2.5"/>
  <line x1="48" y1="46" x2="56" y2="54" stroke="#fbbf24" stroke-width="3" stroke-linecap="round"/>
</svg>""",

    "amass": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <circle cx="32" cy="14" r="6" fill="#a78bfa" stroke="#8b5cf6" stroke-width="2"/>
  <circle cx="14" cy="46" r="6" fill="#a78bfa" stroke="#8b5cf6" stroke-width="2"/>
  <circle cx="50" cy="46" r="6" fill="#a78bfa" stroke="#8b5cf6" stroke-width="2"/>
  <circle cx="32" cy="40" r="5" fill="#38bdf8" stroke="#0284c7" stroke-width="2"/>
  <line x1="32" y1="20" x2="32" y2="35" stroke="#c084fc" stroke-width="2"/>
  <line x1="32" y1="20" x2="18" y2="42" stroke="#c084fc" stroke-width="2"/>
  <line x1="32" y1="20" x2="46" y2="42" stroke="#c084fc" stroke-width="2"/>
  <line x1="18" y1="46" x2="27" y2="42" stroke="#38bdf8" stroke-width="2"/>
  <line x1="46" y1="46" x2="37" y2="42" stroke="#38bdf8" stroke-width="2"/>
  <circle cx="32" cy="28" r="2" fill="#34d399"/>
</svg>""",

    "photon": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <circle cx="32" cy="32" r="26" fill="#0f172a" stroke="#f43f5e" stroke-width="2.5"/>
  <polygon points="34,8 18,34 32,34 30,56 46,30 32,30" fill="#fb7185" stroke="#f43f5e" stroke-width="1.5" stroke-linejoin="round"/>
</svg>""",

    "autopsy": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <circle cx="28" cy="28" r="18" fill="#0f172a" stroke="#fbbf24" stroke-width="3"/>
  <circle cx="28" cy="28" r="10" fill="none" stroke="#f59e0b" stroke-width="1.8" stroke-dasharray="3,2"/>
  <line x1="41" y1="41" x2="56" y2="56" stroke="#fbbf24" stroke-width="4" stroke-linecap="round"/>
  <path d="M22 28 L26 32 L34 24" fill="none" stroke="#34d399" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>""",

    "nikto": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <path d="M32 6 L54 14 V32 C54 46 32 58 32 58 C32 58 10 46 10 32 V14 Z" fill="#0f172a" stroke="#38bdf8" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="M22 30 L30 38 L42 22" fill="none" stroke="#38bdf8" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
</svg>""",

    "sqlmap": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <ellipse cx="32" cy="16" rx="22" ry="8" fill="#1e293b" stroke="#ef4444" stroke-width="2.5"/>
  <path d="M10 16 V32 C10 36 20 40 32 40 C44 40 54 36 54 32 V16" fill="none" stroke="#ef4444" stroke-width="2.5"/>
  <path d="M10 32 V48 C10 52 20 56 32 56 C44 56 54 52 54 48 V32" fill="none" stroke="#ef4444" stroke-width="2.5"/>
  <line x1="20" y1="28" x2="44" y2="28" stroke="#f87171" stroke-width="2" stroke-linecap="round"/>
  <line x1="20" y1="44" x2="38" y2="44" stroke="#f87171" stroke-width="2" stroke-linecap="round"/>
</svg>""",

    "gobuster": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <path d="M8 18 C8 15.7 9.8 14 12 14 H24 L28 20 H52 C54.2 20 56 21.8 56 24 V48 C56 50.2 54.2 52 52 52 H12 C9.8 52 8 50.2 8 48 Z" fill="#0f172a" stroke="#10b981" stroke-width="2.5"/>
  <circle cx="36" cy="36" r="8" fill="#1e293b" stroke="#34d399" stroke-width="2"/>
  <line x1="42" y1="42" x2="50" y2="50" stroke="#34d399" stroke-width="2.5" stroke-linecap="round"/>
</svg>""",

    "wfuzz": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect x="10" y="10" width="44" height="44" rx="6" fill="#0f172a" stroke="#8b5cf6" stroke-width="2.5"/>
  <line x1="10" y1="24" x2="54" y2="24" stroke="#a78bfa" stroke-width="1.5"/>
  <line x1="10" y1="38" x2="54" y2="38" stroke="#a78bfa" stroke-width="1.5"/>
  <line x1="24" y1="10" x2="24" y2="54" stroke="#a78bfa" stroke-width="1.5"/>
  <line x1="38" y1="10" x2="38" y2="54" stroke="#a78bfa" stroke-width="1.5"/>
  <circle cx="31" cy="31" r="5" fill="#f43f5e"/>
</svg>""",

    "whatweb": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect x="8" y="12" width="48" height="40" rx="5" fill="#0f172a" stroke="#3b82f6" stroke-width="2.5"/>
  <line x1="8" y1="22" x2="56" y2="22" stroke="#3b82f6" stroke-width="2"/>
  <circle cx="14" cy="17" r="2" fill="#ef4444"/>
  <circle cx="20" cy="17" r="2" fill="#f59e0b"/>
  <circle cx="26" cy="17" r="2" fill="#10b981"/>
  <text x="14" y="38" font-family="monospace" font-size="12" fill="#60a5fa" font-weight="bold">&lt;/&gt;</text>
  <text x="36" y="44" font-family="sans-serif" font-size="10" fill="#93c5fd">JS</text>
</svg>""",

    "hydra": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect x="18" y="26" width="28" height="30" rx="4" fill="#0f172a" stroke="#f97316" stroke-width="2.5"/>
  <path d="M24 26 V18 C24 13.6 27.6 10 32 10 C36.4 10 40 13.6 40 18 V26" fill="none" stroke="#fb923c" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="32" cy="38" r="3.5" fill="#f97316"/>
  <line x1="32" y1="41.5" x2="32" y2="48" stroke="#f97316" stroke-width="2.5"/>
  <path d="M12 36 L18 36" stroke="#f97316" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M46 36 L52 36" stroke="#f97316" stroke-width="2.5" stroke-linecap="round"/>
</svg>""",

    "john": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect x="16" y="26" width="32" height="30" rx="4" fill="#0f172a" stroke="#dc2626" stroke-width="2.5"/>
  <path d="M22 26 V18 C22 12.5 26.5 8 32 8 C37.5 8 42 12.5 42 18 V22" fill="none" stroke="#ef4444" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="24" y1="41" x2="40" y2="41" stroke="#f87171" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="32" y1="33" x2="32" y2="49" stroke="#f87171" stroke-width="2.5" stroke-linecap="round"/>
</svg>""",

    "hashcat": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect x="14" y="14" width="36" height="36" rx="4" fill="#0f172a" stroke="#e11d48" stroke-width="2.5"/>
  <rect x="22" y="22" width="20" height="20" rx="2" fill="#1e293b" stroke="#f43f5e" stroke-width="2"/>
  <line x1="20" y1="8" x2="20" y2="14" stroke="#e11d48" stroke-width="2"/>
  <line x1="32" y1="8" x2="32" y2="14" stroke="#e11d48" stroke-width="2"/>
  <line x1="44" y1="8" x2="44" y2="14" stroke="#e11d48" stroke-width="2"/>
  <line x1="20" y1="50" x2="20" y2="56" stroke="#e11d48" stroke-width="2"/>
  <line x1="32" y1="50" x2="32" y2="56" stroke="#e11d48" stroke-width="2"/>
  <line x1="44" y1="50" x2="44" y2="56" stroke="#e11d48" stroke-width="2"/>
  <text x="26" y="36" font-family="monospace" font-size="10" fill="#fb7185" font-weight="bold">#</text>
</svg>""",

    "hashid": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <path d="M12 16 H36 L52 32 L36 48 H12 Z" fill="#0f172a" stroke="#6366f1" stroke-width="2.5" stroke-linejoin="round"/>
  <circle cx="22" cy="32" r="4" fill="#818cf8"/>
  <text x="32" y="36" font-family="monospace" font-size="11" fill="#c7d2fe" font-weight="bold">ID</text>
</svg>""",

    "netcat": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect x="8" y="12" width="48" height="40" rx="5" fill="#0f172a" stroke="#10b981" stroke-width="2.5"/>
  <text x="14" y="34" font-family="monospace" font-size="14" fill="#34d399" font-weight="bold">&gt;_</text>
  <text x="34" y="44" font-family="monospace" font-size="12" fill="#6ee7b7" font-weight="bold">nc</text>
</svg>""",

    "wireshark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <path d="M10 44 C20 44 24 24 38 14 C34 24 44 28 54 26 C46 36 34 46 10 44 Z" fill="#0f172a" stroke="#0284c7" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="M8 52 C24 52 38 48 56 48" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4,3"/>
</svg>""",

    "wifite": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <path d="M12 20 C22 10 42 10 52 20" fill="none" stroke="#8b5cf6" stroke-width="3" stroke-linecap="round"/>
  <path d="M18 28 C25 20 39 20 46 28" fill="none" stroke="#a78bfa" stroke-width="3" stroke-linecap="round"/>
  <path d="M24 36 C28 32 36 32 40 36" fill="none" stroke="#c084fc" stroke-width="3" stroke-linecap="round"/>
  <circle cx="32" cy="46" r="4" fill="#8b5cf6"/>
</svg>""",

    "wash": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <line x1="32" y1="20" x2="32" y2="52" stroke="#06b6d4" stroke-width="3" stroke-linecap="round"/>
  <circle cx="32" cy="16" r="4" fill="#22d3ee"/>
  <path d="M20 28 C26 22 38 22 44 28" fill="none" stroke="#06b6d4" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M14 20 C24 10 40 10 50 20" fill="none" stroke="#22d3ee" stroke-width="2.5" stroke-linecap="round"/>
  <rect x="22" y="40" width="20" height="12" rx="2" fill="#0f172a" stroke="#67e8f9" stroke-width="1.8"/>
  <text x="25" y="49" font-family="sans-serif" font-size="8" fill="#67e8f9" font-weight="bold">WPS</text>
</svg>""",

    "reaver": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <circle cx="32" cy="32" r="24" fill="#0f172a" stroke="#ec4899" stroke-width="2.5"/>
  <path d="M24 32 L30 38 L42 22" fill="none" stroke="#f472b6" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="18" y="52" font-family="sans-serif" font-size="9" fill="#f472b6" font-weight="bold">WPS-PIN</text>
</svg>""",

    "sparrow": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <path d="M8 48 C16 48 20 20 28 20 C36 20 40 40 48 40 C52 40 54 30 56 30" fill="none" stroke="#f59e0b" stroke-width="3" stroke-linecap="round"/>
  <line x1="8" y1="52" x2="56" y2="52" stroke="#fbbf24" stroke-width="1.5"/>
  <circle cx="28" cy="20" r="3" fill="#f59e0b"/>
</svg>""",

    "sslscan": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <path d="M32 8 L52 16 V32 C52 44 32 56 32 56 C32 56 12 44 12 32 V16 Z" fill="#0f172a" stroke="#10b981" stroke-width="2.5"/>
  <rect x="24" y="28" width="16" height="14" rx="2" fill="#10b981"/>
  <path d="M27 28 V24 C27 21.2 29.2 19 32 19 C34.8 19 37 21.2 37 24 V28" fill="none" stroke="#34d399" stroke-width="2"/>
</svg>""",

    "sslyze": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <circle cx="32" cy="32" r="22" fill="#0f172a" stroke="#6366f1" stroke-width="2.5"/>
  <path d="M32 14 V32 L42 42" stroke="#818cf8" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="32" cy="32" r="3" fill="#818cf8"/>
</svg>""",

    "tlssled": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <path d="M32 6 L52 14 V30 C52 44 32 56 32 56 C32 56 12 44 12 30 V14 Z" fill="#0f172a" stroke="#14b8a6" stroke-width="2.5"/>
  <text x="20" y="36" font-family="monospace" font-size="11" fill="#2dd4bf" font-weight="bold">TLS</text>
</svg>""",

    "ncrack": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect x="14" y="24" width="36" height="30" rx="5" fill="#0f172a" stroke="#f59e0b" stroke-width="2.5"/>
  <path d="M22 24 V17 C22 11.5 26.5 7 32 7 C37.5 7 42 11.5 42 17 V24" fill="none" stroke="#fbbf24" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="32" cy="36" r="3.5" fill="#f59e0b"/>
  <path d="M32 39.5 L30 46 H34 L32 46" stroke="#f59e0b" stroke-width="2" stroke-linecap="round"/>
  <path d="M38 27 L26 49" stroke="#ef4444" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="2,3"/>
  <circle cx="10" cy="38" r="2.5" fill="#38bdf8"/>
  <circle cx="54" cy="38" r="2.5" fill="#38bdf8"/>
  <line x1="10" y1="38" x2="14" y2="38" stroke="#38bdf8" stroke-width="1.5"/>
  <line x1="50" y1="38" x2="54" y2="38" stroke="#38bdf8" stroke-width="1.5"/>
</svg>"""
}

def ensure_tool_svg_icons() -> None:
    """Writes SVG icon files to disk if they do not exist."""
    icons_dir = get_icons_dir()
    for tool_id, svg_content in TOOL_SVG_MAP.items():
        svg_file = icons_dir / f"{tool_id}.svg"
        if not svg_file.exists():
            try:
                svg_file.write_text(svg_content, encoding="utf-8")
            except Exception as e:
                print(f"[IconManager] Error writing SVG for {tool_id}: {e}")

def get_tool_icon_path(tool_id: str) -> str:
    """
    Returns path to SVG icon file for a tool, generating it if necessary.
    Falls back to a default SVG if specific tool_id is missing.
    """
    ensure_tool_svg_icons()
    icons_dir = get_icons_dir()
    tool_clean = tool_id.lower().strip()
    
    target_path = icons_dir / f"{tool_clean}.svg"
    if target_path.exists():
        return str(target_path)
    
    # Generic fallback SVG if tool icon not found
    fallback_path = icons_dir / "nmap.svg"
    return str(fallback_path) if fallback_path.exists() else ""
