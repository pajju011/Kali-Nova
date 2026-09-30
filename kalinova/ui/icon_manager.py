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
    # Official Kali-Nova Brand Logo (Kali Doc Style)
    # ---------------------------------------------------------
    "kalinova": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_kn" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
    <linearGradient id="cyan_kn" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#0284c7"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_kn)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <path d="M50 16 L76 28 V52 C76 68 50 82 50 82 C50 82 24 68 24 52 V28 Z" fill="#090d16" stroke="#38bdf8" stroke-width="3" stroke-linejoin="round"/>
  <path d="M50 26 C55 33 63 36 63 46 C63 56 54 62 50 67 C46 62 37 56 37 46 C37 36 45 33 50 26 Z" fill="none" stroke="#00e5ff" stroke-width="2.5" stroke-linejoin="round"/>
  <polygon points="50,36 55,46 50,56 45,46" fill="#38bdf8"/>
  <circle cx="50" cy="46" r="3" fill="#ffffff"/>
  <line x1="38" y1="46" x2="62" y2="46" stroke="#00e5ff" stroke-width="2" stroke-opacity="0.8"/>
</svg>""",

    # ---------------------------------------------------------
    # Reconnaissance & OSINT Tools (Official Kali Doc Style)
    # ---------------------------------------------------------
    "nmap": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_nmap" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
    <radialGradient id="iris_nmap" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#7dd3fc"/>
      <stop offset="40%" stop-color="#38bdf8"/>
      <stop offset="80%" stop-color="#0284c7"/>
      <stop offset="100%" stop-color="#0369a1"/>
    </radialGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_nmap)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <path d="M14 50 C26 26 74 26 86 50 C74 74 26 74 14 50 Z" fill="#0284c7" stroke="#38bdf8" stroke-width="4.5" stroke-linejoin="round"/>
  <path d="M20 50 C30 30 70 30 80 50 C70 70 30 70 20 50 Z" fill="#e0f2fe"/>
  <circle cx="50" cy="50" r="19" fill="url(#iris_nmap)" stroke="#38bdf8" stroke-width="2"/>
  <circle cx="50" cy="50" r="13" fill="#38bdf8" fill-opacity="0.4" stroke="#bae6fd" stroke-width="1.5"/>
  <circle cx="50" cy="50" r="7" fill="#0284c7" fill-opacity="0.6"/>
  <line x1="32" y1="50" x2="68" y2="50" stroke="#ffffff" stroke-width="2.8" stroke-linecap="round"/>
  <line x1="50" y1="32" x2="50" y2="68" stroke="#ffffff" stroke-width="2.8" stroke-linecap="round"/>
</svg>""",

    "whois": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_whois" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_whois)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <circle cx="44" cy="50" r="24" fill="#0b1320" stroke="#38bdf8" stroke-width="3"/>
  <ellipse cx="44" cy="50" rx="11" ry="24" fill="none" stroke="#0284c7" stroke-width="2"/>
  <line x1="20" y1="50" x2="68" y2="50" stroke="#0284c7" stroke-width="2"/>
  <line x1="24" y1="38" x2="64" y2="38" stroke="#0284c7" stroke-width="1.5" stroke-opacity="0.8"/>
  <line x1="24" y1="62" x2="64" y2="62" stroke="#0284c7" stroke-width="1.5" stroke-opacity="0.8"/>
  <circle cx="62" cy="58" r="14" fill="#0f172a" stroke="#38bdf8" stroke-width="3"/>
  <line x1="72" y1="68" x2="84" y2="80" stroke="#38bdf8" stroke-width="4.5" stroke-linecap="round"/>
  <circle cx="62" cy="58" r="6" fill="#0284c7" stroke="#bae6fd" stroke-width="1.5"/>
</svg>""",

    "harvester": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_harv" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_harv)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <path d="M22 64 C22 36 44 20 72 20" fill="none" stroke="#38bdf8" stroke-width="4" stroke-linecap="round"/>
  <path d="M34 68 C34 46 50 34 72 34" fill="none" stroke="#0284c7" stroke-width="3.5" stroke-linecap="round"/>
  <line x1="42" y1="48" x2="74" y2="76" stroke="#38bdf8" stroke-width="4" stroke-linecap="round"/>
  <circle cx="74" cy="76" r="7" fill="#0284c7" stroke="#38bdf8" stroke-width="2.5"/>
  <circle cx="28" cy="32" r="5" fill="#38bdf8"/>
  <circle cx="50" cy="22" r="4.5" fill="#00e5ff"/>
  <circle cx="76" cy="36" r="5" fill="#38bdf8"/>
  <rect x="18" y="66" width="26" height="16" rx="3" fill="#0b1320" stroke="#38bdf8" stroke-width="2.5"/>
  <polyline points="18,66 31,76 44,66" fill="none" stroke="#38bdf8" stroke-width="2"/>
</svg>""",

    "metagoofil": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_meta" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_meta)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <rect x="18" y="24" width="38" height="48" rx="5" fill="#0b1320" stroke="#38bdf8" stroke-width="3"/>
  <line x1="26" y1="34" x2="48" y2="34" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="26" y1="44" x2="44" y2="44" stroke="#0284c7" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="26" y1="54" x2="48" y2="54" stroke="#0284c7" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="58" cy="58" r="15" fill="#090d16" stroke="#00e5ff" stroke-width="3"/>
  <line x1="68" y1="68" x2="80" y2="80" stroke="#00e5ff" stroke-width="4.5" stroke-linecap="round"/>
  <text x="49" y="62" font-family="monospace" font-size="11" fill="#38bdf8" font-weight="bold">XML</text>
</svg>""",

    "amass": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_amass" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_amass)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <line x1="50" y1="24" x2="24" y2="68" stroke="#0284c7" stroke-width="3"/>
  <line x1="50" y1="24" x2="76" y2="68" stroke="#0284c7" stroke-width="3"/>
  <line x1="24" y1="68" x2="76" y2="68" stroke="#0284c7" stroke-width="3"/>
  <line x1="50" y1="24" x2="50" y2="52" stroke="#38bdf8" stroke-width="2.5"/>
  <line x1="24" y1="68" x2="50" y2="52" stroke="#38bdf8" stroke-width="2.5"/>
  <line x1="76" y1="68" x2="50" y2="52" stroke="#38bdf8" stroke-width="2.5"/>
  <circle cx="50" cy="24" r="8" fill="#0284c7" stroke="#38bdf8" stroke-width="2.5"/>
  <circle cx="24" cy="68" r="8" fill="#0284c7" stroke="#38bdf8" stroke-width="2.5"/>
  <circle cx="76" cy="68" r="8" fill="#0284c7" stroke="#38bdf8" stroke-width="2.5"/>
  <circle cx="50" cy="52" r="9" fill="#0b1320" stroke="#00e5ff" stroke-width="3"/>
  <circle cx="50" cy="52" r="4" fill="#38bdf8"/>
</svg>""",

    "photon": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_phot" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_phot)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <circle cx="50" cy="50" r="32" fill="#0b1320" stroke="#0284c7" stroke-width="2.5"/>
  <polygon points="56,18 28,52 48,52 42,82 72,46 52,46" fill="#38bdf8" stroke="#00e5ff" stroke-width="2" stroke-linejoin="round"/>
</svg>""",

    "autopsy": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_auto" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_auto)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <circle cx="44" cy="44" r="26" fill="#0b1320" stroke="#38bdf8" stroke-width="3"/>
  <circle cx="44" cy="44" r="16" fill="#05070a" stroke="#0284c7" stroke-width="2"/>
  <circle cx="44" cy="44" r="6" fill="#00e5ff"/>
  <line x1="63" y1="63" x2="82" y2="82" stroke="#38bdf8" stroke-width="5" stroke-linecap="round"/>
  <path d="M54 34 L62 42 L52 52" fill="none" stroke="#00e5ff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
</svg>""",

    # ---------------------------------------------------------
    # Web Testing Tools (Official Kali Doc Style)
    # ---------------------------------------------------------
    "nikto": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_nikto" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_nikto)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <path d="M50 18 L76 28 V50 C76 68 50 80 50 80 C50 80 24 68 24 50 V28 Z" fill="#0b1320" stroke="#38bdf8" stroke-width="3.5" stroke-linejoin="round"/>
  <circle cx="50" cy="46" r="16" fill="none" stroke="#0284c7" stroke-width="2" stroke-dasharray="4,4"/>
  <line x1="50" y1="30" x2="50" y2="62" stroke="#38bdf8" stroke-width="2.5"/>
  <line x1="34" y1="46" x2="66" y2="46" stroke="#38bdf8" stroke-width="2.5"/>
  <circle cx="50" cy="46" r="5" fill="#00e5ff"/>
</svg>""",

    "sqlmap": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_sql" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_sql)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <ellipse cx="46" cy="28" rx="24" ry="9" fill="#0b1320" stroke="#38bdf8" stroke-width="3"/>
  <path d="M22 28 V46 C22 51 33 55 46 55 C59 55 70 51 70 46 V28" fill="none" stroke="#38bdf8" stroke-width="3"/>
  <path d="M22 46 V64 C22 69 33 73 46 73 C59 73 70 69 70 64 V46" fill="none" stroke="#38bdf8" stroke-width="3"/>
  <polygon points="68,22 80,34 62,52 54,50 52,42" fill="#00e5ff" stroke="#38bdf8" stroke-width="2"/>
  <line x1="52" y1="54" x2="42" y2="64" stroke="#bae6fd" stroke-width="3.5" stroke-linecap="round"/>
</svg>""",

    "gobuster": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_go" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="0%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_go)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <path d="M16 28 C16 24.5 19 22 22 22 H40 L46 30 H76 C79.5 30 82 32.5 82 36 V70 C82 73.5 79.5 76 76 76 H22 C19 76 16 73.5 16 70 Z" fill="#0b1320" stroke="#38bdf8" stroke-width="3.5"/>
  <line x1="28" y1="42" x2="28" y2="64" stroke="#00e5ff" stroke-width="3" stroke-linecap="round"/>
  <line x1="28" y1="50" x2="42" y2="50" stroke="#00e5ff" stroke-width="3" stroke-linecap="round"/>
  <line x1="28" y1="62" x2="42" y2="62" stroke="#00e5ff" stroke-width="3" stroke-linecap="round"/>
  <circle cx="58" cy="54" r="11" fill="#05070a" stroke="#38bdf8" stroke-width="3"/>
  <line x1="66" y1="62" x2="76" y2="72" stroke="#38bdf8" stroke-width="4.5" stroke-linecap="round"/>
</svg>""",

    "wfuzz": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_wfuzz" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_wfuzz)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <rect x="18" y="22" width="64" height="56" rx="8" fill="#0b1320" stroke="#38bdf8" stroke-width="3"/>
  <line x1="18" y1="40" x2="82" y2="40" stroke="#0284c7" stroke-width="2"/>
  <line x1="18" y1="58" x2="82" y2="58" stroke="#0284c7" stroke-width="2"/>
  <circle cx="50" cy="49" r="7" fill="#00e5ff"/>
  <text x="24" y="34" font-family="monospace" font-size="10" fill="#38bdf8" font-weight="bold">FUZZ</text>
</svg>""",

    "whatweb": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_ww" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_ww)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <rect x="16" y="22" width="68" height="56" rx="8" fill="#0b1320" stroke="#38bdf8" stroke-width="3"/>
  <line x1="16" y1="36" x2="84" y2="36" stroke="#0284c7" stroke-width="2.5"/>
  <circle cx="24" cy="29" r="3" fill="#38bdf8"/>
  <circle cx="33" cy="29" r="3" fill="#0284c7"/>
  <circle cx="42" cy="29" r="3" fill="#0369a1"/>
  <text x="24" y="58" font-family="monospace" font-size="16" fill="#00e5ff" font-weight="bold">&lt;/&gt;</text>
  <rect x="54" y="44" width="22" height="24" rx="3" fill="#0284c7"/>
  <text x="57" y="60" font-family="sans-serif" font-size="10" fill="#ffffff" font-weight="bold">WEB</text>
</svg>""",

    # ---------------------------------------------------------
    # Authentication & Password Cracking (Official Kali Doc Style)
    # ---------------------------------------------------------
    "hydra": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_hydra" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_hydra)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <path d="M50 74 V50" stroke="#38bdf8" stroke-width="4.5" stroke-linecap="round"/>
  <path d="M50 50 V24 C50 18 56 14 59 14 C62 14 62 22 56 25" fill="none" stroke="#38bdf8" stroke-width="3.5" stroke-linecap="round"/>
  <circle cx="60" cy="15" r="4.5" fill="#00e5ff"/>
  <path d="M50 50 C38 46 26 36 24 22 C22 14 30 14 34 20" fill="none" stroke="#38bdf8" stroke-width="3.5" stroke-linecap="round"/>
  <circle cx="24" cy="18" r="4.5" fill="#00e5ff"/>
  <path d="M50 50 C62 46 74 36 76 22 C78 14 70 14 66 20" fill="none" stroke="#38bdf8" stroke-width="3.5" stroke-linecap="round"/>
  <circle cx="76" cy="18" r="4.5" fill="#00e5ff"/>
  <rect x="34" y="54" width="32" height="24" rx="5" fill="#0b1320" stroke="#38bdf8" stroke-width="3"/>
  <circle cx="50" cy="66" r="4" fill="#00e5ff"/>
</svg>""",

    "john": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_john" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_john)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <rect x="22" y="38" width="56" height="44" rx="6" fill="#0b1320" stroke="#38bdf8" stroke-width="3.5"/>
  <path d="M34 38 V26 C34 17 41 12 50 12 C59 12 66 17 66 26 V32" fill="none" stroke="#00e5ff" stroke-width="4" stroke-linecap="round"/>
  <path d="M36 56 L46 62 L40 70 L56 72" fill="none" stroke="#38bdf8" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="58" cy="52" r="4.5" fill="#00e5ff"/>
</svg>""",

    "hashcat": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_hcat" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_hcat)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <rect x="20" y="24" width="60" height="52" rx="6" fill="#0b1320" stroke="#38bdf8" stroke-width="3.5"/>
  <line x1="32" y1="16" x2="32" y2="24" stroke="#00e5ff" stroke-width="3" stroke-linecap="round"/>
  <line x1="50" y1="16" x2="50" y2="24" stroke="#00e5ff" stroke-width="3" stroke-linecap="round"/>
  <line x1="68" y1="16" x2="68" y2="24" stroke="#00e5ff" stroke-width="3" stroke-linecap="round"/>
  <line x1="32" y1="76" x2="32" y2="84" stroke="#00e5ff" stroke-width="3" stroke-linecap="round"/>
  <line x1="50" y1="76" x2="50" y2="84" stroke="#00e5ff" stroke-width="3" stroke-linecap="round"/>
  <line x1="68" y1="76" x2="68" y2="84" stroke="#00e5ff" stroke-width="3" stroke-linecap="round"/>
  <path d="M50 32 C54 40 62 44 62 56 C62 64 56 68 50 68 C44 68 38 64 38 56 C38 48 44 44 50 32 Z" fill="#0284c7" stroke="#38bdf8" stroke-width="2.5"/>
  <circle cx="50" cy="58" r="4" fill="#ffffff"/>
</svg>""",

    "hashid": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_hid" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_hid)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <path d="M16 26 H56 L78 50 L56 74 H16 Z" fill="#0b1320" stroke="#38bdf8" stroke-width="3.5" stroke-linejoin="round"/>
  <circle cx="34" cy="50" r="7" fill="#00e5ff"/>
  <text x="44" y="57" font-family="monospace" font-size="16" fill="#bae6fd" font-weight="bold">#ID</text>
</svg>""",

    "ncrack": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_ncrack" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_ncrack)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <rect x="22" y="38" width="56" height="42" rx="7" fill="#0b1320" stroke="#38bdf8" stroke-width="3.5"/>
  <path d="M34 38 V26 C34 18 41 12 50 12 C59 12 66 18 66 26 V38" fill="none" stroke="#00e5ff" stroke-width="3.5" stroke-linecap="round"/>
  <polygon points="53,44 42,60 52,60 47,74 62,54 52,54" fill="#38bdf8" stroke="#00e5ff" stroke-width="1.5"/>
</svg>""",

    # ---------------------------------------------------------
    # Network & Wireless Tools (Official Kali Doc Style)
    # ---------------------------------------------------------
    "netcat": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_nc" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_nc)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <rect x="16" y="20" width="68" height="60" rx="8" fill="#0b1320" stroke="#38bdf8" stroke-width="3.5"/>
  <polyline points="26,38 38,50 26,62" fill="none" stroke="#00e5ff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="44" y1="62" x2="58" y2="62" stroke="#00e5ff" stroke-width="4.5" stroke-linecap="round"/>
  <text x="56" y="48" font-family="monospace" font-size="16" fill="#38bdf8" font-weight="bold">nc</text>
</svg>""",

    "wireshark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_ws" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_ws)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <path d="M16 66 C34 66 40 34 60 20 C54 36 68 42 84 40 C68 58 50 70 16 66 Z" fill="#0284c7" stroke="#38bdf8" stroke-width="3.5" stroke-linejoin="round"/>
  <path d="M12 76 C36 76 56 70 88 70" stroke="#00e5ff" stroke-width="3.5" stroke-linecap="round"/>
  <path d="M20 84 C40 84 62 78 82 78" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="5,4"/>
</svg>""",

    "wifite": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_wifite" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_wifite)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <path d="M18 30 C36 14 64 14 82 30" fill="none" stroke="#38bdf8" stroke-width="5" stroke-linecap="round"/>
  <path d="M28 44 C40 32 60 32 72 44" fill="none" stroke="#00e5ff" stroke-width="4.5" stroke-linecap="round"/>
  <path d="M38 58 C44 50 56 50 62 58" fill="none" stroke="#bae6fd" stroke-width="4" stroke-linecap="round"/>
  <circle cx="50" cy="72" r="6" fill="#38bdf8"/>
</svg>""",

    "wash": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_wash" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_wash)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <line x1="50" y1="30" x2="50" y2="80" stroke="#38bdf8" stroke-width="4.5" stroke-linecap="round"/>
  <circle cx="50" cy="24" r="6" fill="#00e5ff"/>
  <path d="M30 38 C42 28 58 28 70 38" fill="none" stroke="#38bdf8" stroke-width="3.5" stroke-linecap="round"/>
  <path d="M20 28 C38 12 62 12 80 28" fill="none" stroke="#00e5ff" stroke-width="3.5" stroke-linecap="round"/>
  <rect x="32" y="60" width="36" height="20" rx="4" fill="#0b1320" stroke="#38bdf8" stroke-width="2.5"/>
  <text x="36" y="74" font-family="sans-serif" font-size="11" fill="#00e5ff" font-weight="bold">WPS</text>
</svg>""",

    "reaver": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_reav" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_reav)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <circle cx="50" cy="50" r="34" fill="#0b1320" stroke="#38bdf8" stroke-width="3.5"/>
  <path d="M34 50 L44 60 L66 36" fill="none" stroke="#00e5ff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="30" y="68" width="40" height="16" rx="3" fill="#0284c7"/>
  <text x="34" y="80" font-family="sans-serif" font-size="10" fill="#ffffff" font-weight="bold">PIN-KEY</text>
</svg>""",

    "sparrow": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_sparrow" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_sparrow)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <path d="M14 68 C24 68 30 26 42 26 C54 26 60 62 72 62 C78 62 82 40 88 40" fill="none" stroke="#38bdf8" stroke-width="4.5" stroke-linecap="round"/>
  <line x1="14" y1="76" x2="88" y2="76" stroke="#00e5ff" stroke-width="2.5"/>
  <circle cx="42" cy="26" r="5" fill="#00e5ff"/>
  <circle cx="72" cy="62" r="5" fill="#38bdf8"/>
</svg>""",

    "sslscan": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_ssl" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_ssl)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <path d="M50 18 L76 28 V50 C76 68 50 80 50 80 C50 80 24 68 24 50 V28 Z" fill="#0b1320" stroke="#38bdf8" stroke-width="3.5"/>
  <rect x="38" y="44" width="24" height="20" rx="3" fill="#0284c7"/>
  <path d="M42 44 V38 C42 33.5 45.5 30 50 30 C54.5 30 58 33.5 58 38 V44" fill="none" stroke="#00e5ff" stroke-width="3.5"/>
</svg>""",

    "sslyze": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_sslyze" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_sslyze)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <circle cx="50" cy="46" r="28" fill="#0b1320" stroke="#38bdf8" stroke-width="3.5"/>
  <path d="M50 24 V46 L64 60" stroke="#00e5ff" stroke-width="4" stroke-linecap="round"/>
  <circle cx="50" cy="46" r="5" fill="#38bdf8"/>
  <text x="30" y="76" font-family="monospace" font-size="11" fill="#00e5ff" font-weight="bold">CIPHER</text>
</svg>""",

    "tlssled": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="bg_tlssled" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#05070a"/>
    </linearGradient>
  </defs>
  <rect x="8" y="8" width="84" height="84" rx="18" fill="url(#bg_tlssled)" stroke="#1e293b" stroke-width="2.5"/>
  <line x1="24" y1="8" x2="24" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="40" y1="8" x2="40" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="60" y1="8" x2="60" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="76" y1="8" x2="76" y2="92" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="24" x2="92" y2="24" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="40" x2="92" y2="40" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="60" x2="92" y2="60" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <line x1="8" y1="76" x2="92" y2="76" stroke="#162438" stroke-width="1.2" stroke-opacity="0.6"/>
  <rect x="68" y="18" width="14" height="3" rx="1.5" fill="#38bdf8" fill-opacity="0.9"/>
  <rect x="68" y="24" width="14" height="3" rx="1.5" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="68" y="30" width="14" height="3" rx="1.5" fill="#0369a1" fill-opacity="0.7"/>
  <path d="M50 18 L76 28 V48 C76 66 50 78 50 78 C50 78 24 66 24 48 V28 Z" fill="#0b1320" stroke="#38bdf8" stroke-width="3.5"/>
  <text x="32" y="54" font-family="monospace" font-size="16" fill="#00e5ff" font-weight="bold">TLS</text>
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
