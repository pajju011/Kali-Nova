"""
Kali-Nova: Next-Generation AI-Augmented Security & Penetration Testing Framework.
"""

import os
import sys

# Ensure internal package submodules (core, ui, modules, etc.) resolve seamlessly
_PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
if _PACKAGE_DIR not in sys.path:
    sys.path.insert(0, _PACKAGE_DIR)

__version__ = "1.0.0"
__author__ = "Kali-Nova Team"
__license__ = "GPL-3.0"

from core.database import DatabaseManager
from core.risk_engine import RiskEngine
from core.port_parser import PortParser
from core.ai_copilot import AICopilot
from core.suggestion_engine import SuggestionEngine

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "DatabaseManager",
    "RiskEngine",
    "PortParser",
    "AICopilot",
    "SuggestionEngine",
]
