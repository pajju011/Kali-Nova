"""
Icon Manager for Kali-Nova.
Generates and manages professional vector SVG icons for all security tools and navigation menus.
Adheres to official Kali Linux security tooling motifs with sleek dark-mode vector iconography.
"""

import os
from pathlib import Path
from typing import Dict, Optional

def get_icons_dir() -> Path:
    """Returns absolute path to resources/icons directory."""
    base_dir = Path(__file__).parent.parent / "resources" / "icons"
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir

TOOL_SVG_MAP: Dict[str, str] = {
    # ---------------------------------------------------------
    # Official Kali-Nova Brand & System Logos
    # ---------------------------------------------------------
    "kalinova": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <defs>
    <linearGradient id="kaliGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00f0ff"/>
      <stop offset="50%" stop-color="#3b82f6"/>
      <stop offset="100%" stop-color="#7c3aed"/>
    </linearGradient>
  </defs>
  <path d="M32 4 L56 14 V32 C56 48 32 60 32 60 C32 60 8 48 8 32 V14 Z" fill="#0b1220" stroke="url(#kaliGrad)" stroke-width="2.8" stroke-linejoin="round"/>
  <path d="M32 12 C36 18 44 20 44 28 C44 36 36 42 32 46 C28 42 20 36 20 28 C20 20 28 18 32 12 Z" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linejoin="round"/>
  <polygon points="32,20 36,28 32,36 28,28" fill="#38bdf8"/>
  <circle cx="32" cy="28" r="2.5" fill="#f8fafc"/>
  <line x1="22" y1="28" x2="42" y2="28" stroke="#00f0ff" stroke-width="1.5" stroke-opacity="0.7"/>
</svg>""",

    # ---------------------------------------------------------
    # Reconnaissance & OSINT Tools
    # ---------------------------------------------------------
    "nmap": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <defs>
    <radialGradient id="nmapGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#0284c7" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#0f172a" stop-opacity="0.9"/>
    </radialGradient>
    <linearGradient id="sweepGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#0284c7" stop-opacity="0.0"/>
    </linearGradient>
  </defs>
  <circle cx="32" cy="32" r="28" fill="url(#nmapGrad)" stroke="#38bdf8" stroke-width="2.5"/>
  <circle cx="32" cy="32" r="20" fill="none" stroke="#0284c7" stroke-width="1.5" stroke-dasharray="4,3"/>
  <circle cx="32" cy="32" r="11" fill="none" stroke="#0369a1" stroke-width="1.5"/>
  <line x1="32" y1="4" x2="32" y2="60" stroke="#38bdf8" stroke-width="1.2" stroke-opacity="0.5"/>
  <line x1="4" y1="32" x2="60" y2="32" stroke="#38bdf8" stroke-width="1.2" stroke-opacity="0.5"/>
  <polygon points="32,32 54,14 50,32" fill="url(#sweepGrad)"/>
  <circle cx="45" cy="19" r="3.5" fill="#f43f5e"/>
  <circle cx="20" cy="42" r="2.5" fill="#38bdf8"/>
  <circle cx="24" cy="20" r="2" fill="#34d399"/>
  <circle cx="32" cy="32" r="3" fill="#38bdf8"/>
</svg>""",

    "whois": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <circle cx="32" cy="32" r="27" fill="#0f172a" stroke="#818cf8" stroke-width="2.5"/>
  <ellipse cx="32" cy="32" rx="13" ry="27" fill="none" stroke="#6366f1" stroke-width="1.8"/>
  <line x1="5" y1="32" x2="59" y2="32" stroke="#6366f1" stroke-width="1.8"/>
  <line x1="10" y1="18" x2="54" y2="18" stroke="#818cf8" stroke-width="1.2" stroke-opacity="0.7"/>
  <line x1="10" y1="46" x2="54" y2="46" stroke="#818cf8" stroke-width="1.2" stroke-opacity="0.7"/>
  <rect x="34" y="24" width="22" height="26" rx="4" fill="#1e1b4b" stroke="#a78bfa" stroke-width="2"/>
  <line x1="38" y1="30" x2="52" y2="30" stroke="#c4b5fd" stroke-width="1.8" stroke-linecap="round"/>
  <line x1="38" y1="36" x2="48" y2="36" stroke="#c4b5fd" stroke-width="1.8" stroke-linecap="round"/>
  <line x1="38" y1="42" x2="50" y2="42" stroke="#c4b5fd" stroke-width="1.8" stroke-linecap="round"/>
  <circle cx="48" cy="18" r="4" fill="#a78bfa"/>
</svg>""",

    "harvester": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <path d="M12 40 C12 22 26 10 44 10" fill="none" stroke="#f59e0b" stroke-width="3" stroke-linecap="round"/>
  <path d="M20 44 C20 30 30 20 44 20" fill="none" stroke="#fbbf24" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="28" y1="28" x2="48" y2="48" stroke="#f59e0b" stroke-width="3" stroke-linecap="round"/>
  <circle cx="48" cy="48" r="5" fill="#d97706" stroke="#fbbf24" stroke-width="2"/>
  <circle cx="16" cy="18" r="3.5" fill="#38bdf8"/>
  <circle cx="32" cy="12" r="3" fill="#34d399"/>
  <circle cx="50" cy="22" r="3.5" fill="#f43f5e"/>
  <line x1="16" y1="18" x2="28" y2="28" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="2,2"/>
  <line x1="32" y1="12" x2="36" y2="22" stroke="#34d399" stroke-width="1.2" stroke-dasharray="2,2"/>
  <rect x="8" y="44" width="18" height="12" rx="2" fill="#0f172a" stroke="#f59e0b" stroke-width="1.8"/>
  <polyline points="8,44 17,51 26,44" fill="none" stroke="#f59e0b" stroke-width="1.5"/>
</svg>""",

    "metagoofil": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect x="10" y="16" width="30" height="38" rx="4" fill="#0f172a" stroke="#059669" stroke-width="2"/>
  <rect x="18" y="10" width="30" height="38" rx="4" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
  <line x1="24" y1="18" x2="42" y2="18" stroke="#34d399" stroke-width="2" stroke-linecap="round"/>
  <line x1="24" y1="24" x2="38" y2="24" stroke="#34d399" stroke-width="2" stroke-linecap="round"/>
  <line x1="24" y1="30" x2="42" y2="30" stroke="#34d399" stroke-width="2" stroke-linecap="round"/>
  <circle cx="44" cy="40" r="10" fill="#0f172a" stroke="#fbbf24" stroke-width="2.5"/>
  <line x1="51" y1="47" x2="59" y2="55" stroke="#fbbf24" stroke-width="3.5" stroke-linecap="round"/>
  <text x="38" y="44" font-family="monospace" font-size="9" fill="#34d399" font-weight="bold">XML</text>
</svg>""",

    "amass": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <line x1="32" y1="14" x2="14" y2="44" stroke="#7c3aed" stroke-width="2"/>
  <line x1="32" y1="14" x2="50" y2="44" stroke="#7c3aed" stroke-width="2"/>
  <line x1="14" y1="44" x2="50" y2="44" stroke="#7c3aed" stroke-width="2"/>
  <line x1="32" y1="14" x2="32" y2="34" stroke="#c084fc" stroke-width="2"/>
  <line x1="14" y1="44" x2="32" y2="34" stroke="#c084fc" stroke-width="2"/>
  <line x1="50" y1="44" x2="32" y2="34" stroke="#c084fc" stroke-width="2"/>
  <circle cx="32" cy="14" r="6" fill="#8b5cf6" stroke="#c084fc" stroke-width="2"/>
  <circle cx="14" cy="44" r="6" fill="#8b5cf6" stroke="#c084fc" stroke-width="2"/>
  <circle cx="50" cy="44" r="6" fill="#8b5cf6" stroke="#c084fc" stroke-width="2"/>
  <circle cx="32" cy="34" r="6" fill="#0284c7" stroke="#38bdf8" stroke-width="2"/>
  <circle cx="23" cy="24" r="2.5" fill="#34d399"/>
  <circle cx="41" cy="24" r="2.5" fill="#34d399"/>
  <circle cx="32" cy="48" r="2.5" fill="#f43f5e"/>
</svg>""",

    "photon": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <circle cx="32" cy="32" r="27" fill="#0f172a" stroke="#f43f5e" stroke-width="2.5"/>
  <polygon points="36,8 18,32 32,32 28,56 46,28 32,28" fill="#f43f5e" stroke="#fb7185" stroke-width="1.5" stroke-linejoin="round"/>
  <circle cx="18" cy="18" r="2" fill="#fb7185"/>
  <circle cx="46" cy="46" r="2" fill="#fb7185"/>
</svg>""",

    "autopsy": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <circle cx="28" cy="28" r="20" fill="#0f172a" stroke="#f59e0b" stroke-width="2.5"/>
  <circle cx="28" cy="28" r="12" fill="#1e293b" stroke="#d97706" stroke-width="1.8"/>
  <circle cx="28" cy="28" r="4" fill="#fbbf24"/>
  <line x1="28" y1="8" x2="28" y2="16" stroke="#f59e0b" stroke-width="1.5"/>
  <line x1="28" y1="40" x2="28" y2="48" stroke="#f59e0b" stroke-width="1.5"/>
  <line x1="8" y1="28" x2="16" y2="28" stroke="#f59e0b" stroke-width="1.5"/>
  <line x1="40" y1="28" x2="48" y2="28" stroke="#f59e0b" stroke-width="1.5"/>
  <circle cx="38" cy="38" r="11" fill="#0f172a" stroke="#38bdf8" stroke-width="2.5"/>
  <line x1="46" y1="46" x2="57" y2="57" stroke="#38bdf8" stroke-width="4" stroke-linecap="round"/>
  <path d="M34 38 L37 41 L43 35" fill="none" stroke="#34d399" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>""",

    # ---------------------------------------------------------
    # Web Testing Tools
    # ---------------------------------------------------------
    "nikto": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <path d="M32 6 L54 14 V32 C54 46 32 58 32 58 C32 58 10 46 10 32 V14 Z" fill="#0f172a" stroke="#38bdf8" stroke-width="2.5" stroke-linejoin="round"/>
  <circle cx="32" cy="28" r="12" fill="none" stroke="#0284c7" stroke-width="1.5" stroke-dasharray="3,3"/>
  <line x1="32" y1="16" x2="32" y2="40" stroke="#38bdf8" stroke-width="1.5"/>
  <line x1="20" y1="28" x2="44" y2="28" stroke="#38bdf8" stroke-width="1.5"/>
  <circle cx="32" cy="28" r="3.5" fill="#f43f5e"/>
</svg>""",

    "sqlmap": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <ellipse cx="32" cy="15" rx="20" ry="7" fill="#1e293b" stroke="#ef4444" stroke-width="2.5"/>
  <path d="M12 15 V30 C12 34 21 37 32 37 C43 37 52 34 52 30 V15" fill="none" stroke="#ef4444" stroke-width="2.5"/>
  <path d="M12 30 V45 C12 49 21 52 32 52 C43 52 52 49 52 45 V30" fill="none" stroke="#ef4444" stroke-width="2.5"/>
  <polygon points="46,8 56,18 42,32 36,30 34,24" fill="#ef4444" stroke="#f87171" stroke-width="1.5"/>
  <line x1="34" y1="34" x2="26" y2="42" stroke="#fca5a5" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="24" cy="44" r="2" fill="#ef4444"/>
</svg>""",

    "gobuster": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <path d="M8 18 C8 15.7 9.8 14 12 14 H24 L28 20 H52 C54.2 20 56 21.8 56 24 V48 C56 50.2 54.2 52 52 52 H12 C9.8 52 8 50.2 8 48 Z" fill="#0f172a" stroke="#10b981" stroke-width="2.5"/>
  <line x1="18" y1="28" x2="18" y2="44" stroke="#34d399" stroke-width="2"/>
  <line x1="18" y1="34" x2="28" y2="34" stroke="#34d399" stroke-width="2"/>
  <line x1="18" y1="42" x2="28" y2="42" stroke="#34d399" stroke-width="2"/>
  <circle cx="38" cy="36" r="8" fill="#1e293b" stroke="#34d399" stroke-width="2.2"/>
  <line x1="44" y1="42" x2="52" y2="50" stroke="#34d399" stroke-width="3" stroke-linecap="round"/>
</svg>""",

    "wfuzz": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect x="8" y="10" width="48" height="44" rx="6" fill="#0f172a" stroke="#8b5cf6" stroke-width="2.5"/>
  <line x1="8" y1="24" x2="56" y2="24" stroke="#a78bfa" stroke-width="1.5"/>
  <line x1="8" y1="38" x2="56" y2="38" stroke="#a78bfa" stroke-width="1.5"/>
  <line x1="24" y1="10" x2="24" y2="54" stroke="#a78bfa" stroke-width="1.5"/>
  <line x1="40" y1="10" x2="40" y2="54" stroke="#a78bfa" stroke-width="1.5"/>
  <circle cx="32" cy="31" r="5" fill="#f43f5e"/>
  <text x="12" y="20" font-family="monospace" font-size="8" fill="#c084fc" font-weight="bold">FUZZ</text>
</svg>""",

    "whatweb": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect x="6" y="12" width="52" height="40" rx="6" fill="#0f172a" stroke="#3b82f6" stroke-width="2.5"/>
  <line x1="6" y1="22" x2="58" y2="22" stroke="#3b82f6" stroke-width="2"/>
  <circle cx="12" cy="17" r="2" fill="#ef4444"/>
  <circle cx="18" cy="17" r="2" fill="#f59e0b"/>
  <circle cx="24" cy="17" r="2" fill="#10b981"/>
  <text x="12" y="38" font-family="monospace" font-size="12" fill="#60a5fa" font-weight="bold">&lt;/&gt;</text>
  <rect x="36" y="28" width="16" height="18" rx="2" fill="#1e3a8a"/>
  <text x="39" y="41" font-family="sans-serif" font-size="9" fill="#93c5fd" font-weight="bold">TECH</text>
</svg>""",

    # ---------------------------------------------------------
    # Authentication & Cracking Tools
    # ---------------------------------------------------------
    "hydra": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <path d="M32 54 V36" stroke="#f97316" stroke-width="3" stroke-linecap="round"/>
  <path d="M32 36 V16 C32 12 36 8 38 8 C40 8 40 14 36 16" fill="none" stroke="#fb923c" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="38" cy="9" r="3" fill="#ea580c"/>
  <path d="M32 36 C24 34 16 26 14 16 C12 10 18 10 20 14" fill="none" stroke="#fb923c" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="15" cy="12" r="3" fill="#ea580c"/>
  <path d="M32 36 C40 34 48 26 50 16 C52 10 46 10 44 14" fill="none" stroke="#fb923c" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="49" cy="12" r="3" fill="#ea580c"/>
  <rect x="20" y="38" width="24" height="18" rx="4" fill="#0f172a" stroke="#f97316" stroke-width="2.2"/>
  <circle cx="32" cy="46" r="3" fill="#fb923c"/>
</svg>""",

    "john": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect x="14" y="24" width="36" height="32" rx="4" fill="#0f172a" stroke="#dc2626" stroke-width="2.5"/>
  <path d="M22 24 V16 C22 10.5 26.5 6 32 6 C37.5 6 42 10.5 42 16 V20" fill="none" stroke="#ef4444" stroke-width="3" stroke-linecap="round"/>
  <path d="M24 38 L30 42 L26 48 L36 50" fill="none" stroke="#f87171" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="38" cy="34" r="3" fill="#ef4444"/>
</svg>""",

    "hashcat": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect x="12" y="14" width="40" height="36" rx="4" fill="#0f172a" stroke="#e11d48" stroke-width="2.5"/>
  <line x1="20" y1="8" x2="20" y2="14" stroke="#e11d48" stroke-width="2.2"/>
  <line x1="32" y1="8" x2="32" y2="14" stroke="#e11d48" stroke-width="2.2"/>
  <line x1="44" y1="8" x2="44" y2="14" stroke="#e11d48" stroke-width="2.2"/>
  <line x1="20" y1="50" x2="20" y2="56" stroke="#e11d48" stroke-width="2.2"/>
  <line x1="32" y1="50" x2="32" y2="56" stroke="#e11d48" stroke-width="2.2"/>
  <line x1="44" y1="50" x2="44" y2="56" stroke="#e11d48" stroke-width="2.2"/>
  <path d="M32 20 C34 26 40 28 40 36 C40 41 36 44 32 44 C28 44 24 41 24 36 C24 31 28 28 32 20 Z" fill="#f43f5e" stroke="#fb7185" stroke-width="1.5"/>
  <circle cx="32" cy="38" r="2.5" fill="#fef08a"/>
</svg>""",

    "hashid": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <path d="M10 16 H36 L52 32 L36 48 H10 Z" fill="#0f172a" stroke="#6366f1" stroke-width="2.5" stroke-linejoin="round"/>
  <circle cx="22" cy="32" r="4.5" fill="#818cf8"/>
  <text x="30" y="37" font-family="monospace" font-size="12" fill="#c7d2fe" font-weight="bold">#ID</text>
</svg>""",

    "ncrack": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect x="14" y="24" width="36" height="30" rx="5" fill="#0f172a" stroke="#f59e0b" stroke-width="2.5"/>
  <path d="M22 24 V17 C22 11.5 26.5 7 32 7 C37.5 7 42 11.5 42 17 V24" fill="none" stroke="#fbbf24" stroke-width="2.5" stroke-linecap="round"/>
  <polygon points="34,28 26,40 33,40 30,50 40,36 33,36" fill="#f59e0b" stroke="#fbbf24" stroke-width="1.2"/>
  <circle cx="8" cy="38" r="3" fill="#38bdf8"/>
  <circle cx="56" cy="38" r="3" fill="#38bdf8"/>
  <line x1="8" y1="38" x2="14" y2="38" stroke="#38bdf8" stroke-width="2"/>
  <line x1="50" y1="38" x2="56" y2="38" stroke="#38bdf8" stroke-width="2"/>
</svg>""",

    # ---------------------------------------------------------
    # Network & Wireless Tools
    # ---------------------------------------------------------
    "netcat": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect x="6" y="12" width="52" height="40" rx="6" fill="#0f172a" stroke="#10b981" stroke-width="2.5"/>
  <polyline points="14,24 22,32 14,40" fill="none" stroke="#34d399" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="26" y1="40" x2="36" y2="40" stroke="#34d399" stroke-width="3" stroke-linecap="round"/>
  <text x="36" y="32" font-family="monospace" font-size="12" fill="#6ee7b7" font-weight="bold">nc</text>
</svg>""",

    "wireshark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <path d="M10 44 C22 44 26 22 38 12 C34 24 44 28 54 26 C44 38 32 46 10 44 Z" fill="#0284c7" stroke="#38bdf8" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="M6 50 C22 50 36 46 58 46" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M12 56 C26 56 40 52 54 52" stroke="#0284c7" stroke-width="2" stroke-linecap="round" stroke-dasharray="4,3"/>
</svg>""",

    "wifite": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <path d="M10 18 C22 8 42 8 54 18" fill="none" stroke="#8b5cf6" stroke-width="3.5" stroke-linecap="round"/>
  <path d="M16 26 C25 18 39 18 48 26" fill="none" stroke="#a78bfa" stroke-width="3" stroke-linecap="round"/>
  <path d="M22 34 C28 28 36 28 42 34" fill="none" stroke="#c084fc" stroke-width="3" stroke-linecap="round"/>
  <circle cx="32" cy="46" r="4.5" fill="#8b5cf6" stroke="#c084fc" stroke-width="2"/>
  <line x1="32" y1="46" x2="32" y2="38" stroke="#34d399" stroke-width="2.5" stroke-linecap="round"/>
</svg>""",

    "wash": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <line x1="32" y1="20" x2="32" y2="54" stroke="#06b6d4" stroke-width="3.5" stroke-linecap="round"/>
  <circle cx="32" cy="16" r="4.5" fill="#22d3ee"/>
  <path d="M18 28 C26 20 38 20 46 28" fill="none" stroke="#06b6d4" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M12 20 C24 8 40 8 52 20" fill="none" stroke="#22d3ee" stroke-width="2.5" stroke-linecap="round"/>
  <rect x="20" y="40" width="24" height="14" rx="3" fill="#0f172a" stroke="#67e8f9" stroke-width="1.8"/>
  <text x="23" y="50" font-family="sans-serif" font-size="8" fill="#67e8f9" font-weight="bold">WPS</text>
</svg>""",

    "reaver": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <circle cx="32" cy="32" r="26" fill="#0f172a" stroke="#ec4899" stroke-width="2.5"/>
  <path d="M22 32 L28 38 L42 22" fill="none" stroke="#f472b6" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="18" y="44" width="28" height="12" rx="2" fill="#831843"/>
  <text x="21" y="53" font-family="sans-serif" font-size="8" fill="#fbcfe8" font-weight="bold">PIN-KEY</text>
</svg>""",

    "sparrow": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <path d="M6 46 C14 46 18 16 26 16 C34 16 38 42 46 42 C50 42 54 26 58 26" fill="none" stroke="#f59e0b" stroke-width="3.5" stroke-linecap="round"/>
  <line x1="6" y1="52" x2="58" y2="52" stroke="#fbbf24" stroke-width="1.8"/>
  <circle cx="26" cy="16" r="3.5" fill="#f59e0b"/>
  <circle cx="46" cy="42" r="3.5" fill="#f59e0b"/>
</svg>""",

    "sslscan": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <path d="M32 6 L52 14 V32 C52 46 32 58 32 58 C32 58 12 46 12 32 V14 Z" fill="#0f172a" stroke="#10b981" stroke-width="2.5"/>
  <rect x="24" y="28" width="16" height="14" rx="2" fill="#10b981"/>
  <path d="M27 28 V24 C27 21.2 29.2 19 32 19 C34.8 19 37 21.2 37 24 V28" fill="none" stroke="#34d399" stroke-width="2.5"/>
</svg>""",

    "sslyze": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <circle cx="32" cy="32" r="24" fill="#0f172a" stroke="#6366f1" stroke-width="2.5"/>
  <path d="M32 14 V32 L42 42" stroke="#818cf8" stroke-width="3" stroke-linecap="round"/>
  <circle cx="32" cy="32" r="4" fill="#818cf8"/>
  <text x="18" y="50" font-family="monospace" font-size="8" fill="#a5b4fc" font-weight="bold">CIPHER</text>
</svg>""",

    "tlssled": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <path d="M32 6 L52 14 V30 C52 44 32 56 32 56 C32 56 12 44 12 30 V14 Z" fill="#0f172a" stroke="#14b8a6" stroke-width="2.5"/>
  <text x="18" y="36" font-family="monospace" font-size="11" fill="#2dd4bf" font-weight="bold">TLS</text>
</svg>""",

    # ---------------------------------------------------------
    # Navigation & System SVGs (for Sidebar & TopBar)
    # ---------------------------------------------------------
    "nav_dashboard": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="3" y="3" width="7" height="9" rx="1"/>
  <rect x="14" y="3" width="7" height="5" rx="1"/>
  <rect x="14" y="12" width="7" height="9" rx="1"/>
  <rect x="3" y="16" width="7" height="5" rx="1"/>
</svg>""",

    "nav_recon": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#60a5fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="9"/>
  <circle cx="12" cy="12" r="5"/>
  <line x1="12" y1="2" x2="12" y2="4"/>
  <line x1="12" y1="20" x2="12" y2="22"/>
  <line x1="2" y1="12" x2="4" y2="12"/>
  <line x1="20" y1="12" x2="22" y2="12"/>
</svg>""",

    "nav_web": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#f87171" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <line x1="2" y1="12" x2="22" y2="12"/>
  <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
</svg>""",

    "nav_auth": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#fbbf24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
  <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
  <circle cx="12" cy="16" r="1"/>
</svg>""",

    "nav_network": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="2" y="2" width="6" height="6" rx="1"/>
  <rect x="16" y="2" width="6" height="6" rx="1"/>
  <rect x="9" y="16" width="6" height="6" rx="1"/>
  <path d="M5 8v3a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8"/>
  <path d="M12 12v4"/>
</svg>""",

    "nav_reports": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
  <polyline points="14 2 14 8 20 8"/>
  <line x1="16" y1="13" x2="8" y2="13"/>
  <line x1="16" y1="17" x2="8" y2="17"/>
  <polyline points="10 9 9 9 8 9"/>
</svg>""",

    "nav_settings": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="3"/>
  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
</svg>""",

    "nav_output": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="4 17 10 11 4 5"/>
  <line x1="12" y1="19" x2="20" y2="19"/>
</svg>""",

    "nav_copilot": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#ec4899" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
  <circle cx="12" cy="12" r="3"/>
</svg>"""
}

def ensure_tool_svg_icons(force: bool = False) -> None:
    """Writes SVG icon files to disk, updating if force is True or file missing."""
    icons_dir = get_icons_dir()
    for tool_id, svg_content in TOOL_SVG_MAP.items():
        svg_file = icons_dir / f"{tool_id}.svg"
        if force or not svg_file.exists():
            try:
                svg_file.write_text(svg_content.strip(), encoding="utf-8")
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
    
    # Check direct name match
    target_path = icons_dir / f"{tool_clean}.svg"
    if target_path.exists():
        return str(target_path)
        
    # Alias matches
    aliases = {
        "harvester": "harvester",
        "theharvester": "harvester",
        "sparrowwifi": "sparrow",
        "hash_identifier": "hashid",
    }
    alias_key = aliases.get(tool_clean)
    if alias_key:
        alias_path = icons_dir / f"{alias_key}.svg"
        if alias_path.exists():
            return str(alias_path)
    
    # Generic fallback SVG if tool icon not found
    fallback_path = icons_dir / "nmap.svg"
    return str(fallback_path) if fallback_path.exists() else ""

def get_nav_icon_path(nav_id: str) -> str:
    """
    Returns path to SVG navigation icon.
    """
    ensure_tool_svg_icons()
    icons_dir = get_icons_dir()
    clean_id = nav_id.lower().strip()
    if not clean_id.startswith("nav_"):
        clean_id = f"nav_{clean_id}"
        
    target_path = icons_dir / f"{clean_id}.svg"
    if target_path.exists():
        return str(target_path)
    return ""
