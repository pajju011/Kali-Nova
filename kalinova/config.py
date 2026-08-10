import json
import os
from pathlib import Path

def get_config_dir() -> Path:
    """Returns user-isolated configuration directory adhering to XDG standard on Linux / APPDATA on Windows."""
    if os.name == 'nt':
        base_dir = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        base_dir = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    
    config_dir = base_dir / "kalinova"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir

def get_config_file() -> Path:
    return get_config_dir() / "config.json"

DEFAULT_CONFIG = {
    "ai_provider": "heuristic",  # Options: 'ollama', 'gemini', 'openai', 'heuristic'
    "api_key": "",
    "model": "gemini-1.5-flash",
    "ollama_url": "http://localhost:11434",
    "app_mode": "Professional"
}

def load_config() -> dict:
    """Load configuration from user-isolated JSON file, creating default if not exists."""
    config_file = get_config_file()
    if not config_file.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure all default keys exist
            merged = DEFAULT_CONFIG.copy()
            merged.update(data)
            return merged
    except Exception as e:
        print(f"[Config] Error loading config, returning defaults: {e}")
        return DEFAULT_CONFIG.copy()

def save_config(config_data: dict) -> bool:
    """Save configuration to user-isolated JSON file."""
    config_file = get_config_file()
    try:
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4)
        return True
    except Exception as e:
        print(f"[Config] Error saving config: {e}")
        return False
