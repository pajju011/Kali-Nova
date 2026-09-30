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
    "ai_provider": "gemini",  # Options: 'ollama', 'gemini', 'openai', 'heuristic'
    "api_key": "",
    "model": "gemini-2.0-flash",
    "ollama_url": "http://localhost:11434",
    "app_mode": "Professional",
    "auto_elevate_root": True,
    "elevation_method": "auto"  # Options: 'auto', 'pkexec', 'sudo', 'none'
}

import base64
import hashlib
import hmac

KEYRING_SERVICE = "kalinova_security_suite"

def _derive_keystore_key() -> bytes:
    machine_id = os.environ.get("COMPUTERNAME", "") + os.environ.get("USERNAME", "") + os.environ.get("USER", "")
    salt = b"kalinova_secure_keyring_salt_v1"
    return hashlib.sha256(machine_id.encode("utf-8") + salt).digest()

def _encrypt_credential(text: str) -> str:
    if not text:
        return ""
    key = _derive_keystore_key()
    iv = os.urandom(16)
    data = text.encode("utf-8")
    keystream = bytearray()
    counter = 0
    while len(keystream) < len(data):
        block = hmac.new(key, iv + counter.to_bytes(4, "big"), hashlib.sha256).digest()
        keystream.extend(block)
        counter += 1
    cipher = bytes(d ^ k for d, k in zip(data, keystream[:len(data)]))
    tag = hmac.new(key, iv + cipher, hashlib.sha256).digest()[:16]
    return "ENC:v1:" + base64.b64encode(iv + tag + cipher).decode("utf-8")

def _decrypt_credential(enc_text: str) -> str:
    if not enc_text or not enc_text.startswith("ENC:v1:"):
        return enc_text
    try:
        key = _derive_keystore_key()
        raw = base64.b64decode(enc_text[7:])
        if len(raw) < 32:
            return ""
        iv, tag, cipher = raw[:16], raw[16:32], raw[32:]
        expected_tag = hmac.new(key, iv + cipher, hashlib.sha256).digest()[:16]
        if not hmac.compare_digest(tag, expected_tag):
            return ""
        keystream = bytearray()
        counter = 0
        while len(keystream) < len(cipher):
            block = hmac.new(key, iv + counter.to_bytes(4, "big"), hashlib.sha256).digest()
            keystream.extend(block)
            counter += 1
        plain = bytes(c ^ k for c, k in zip(cipher, keystream[:len(cipher)]))
        return plain.decode("utf-8", errors="replace")
    except Exception:
        return ""

def get_keystore_file() -> Path:
    return get_config_dir() / "keystore.enc"

def set_keyring_api_key(provider: str, api_key: str) -> bool:
    """Securely store an API key into OS Keyring or machine-encrypted keystore."""
    provider_clean = (provider or "default").lower().strip()
    # 1. Try native OS keyring module if installed
    try:
        import keyring
        keyring.set_password(KEYRING_SERVICE, provider_clean, api_key)
        return True
    except Exception:
        pass

    # 2. Fallback to machine-bound encrypted keystore
    try:
        keystore_file = get_keystore_file()
        store = {}
        if keystore_file.exists():
            try:
                with open(keystore_file, "r", encoding="utf-8") as f:
                    store = json.load(f)
            except Exception:
                store = {}
        store[provider_clean] = _encrypt_credential(api_key)
        with open(keystore_file, "w", encoding="utf-8") as f:
            json.dump(store, f, indent=2)
        return True
    except Exception:
        return False

def get_keyring_api_key(provider: str) -> str:
    """Retrieve stored API key from OS Keyring or machine-encrypted keystore."""
    provider_clean = (provider or "default").lower().strip()
    # 1. Try native OS keyring
    try:
        import keyring
        val = keyring.get_password(KEYRING_SERVICE, provider_clean)
        if val:
            return val.strip()
    except Exception:
        pass

    # 2. Fallback to machine-bound encrypted keystore
    try:
        keystore_file = get_keystore_file()
        if keystore_file.exists():
            with open(keystore_file, "r", encoding="utf-8") as f:
                store = json.load(f)
            enc_val = store.get(provider_clean, "")
            if enc_val:
                return _decrypt_credential(enc_val).strip()
    except Exception:
        pass
    return ""

def delete_keyring_api_key(provider: str) -> bool:
    """Delete stored API key from OS Keyring and local encrypted keystore."""
    provider_clean = (provider or "default").lower().strip()
    success = False
    try:
        import keyring
        keyring.delete_password(KEYRING_SERVICE, provider_clean)
        success = True
    except Exception:
        pass

    try:
        keystore_file = get_keystore_file()
        if keystore_file.exists():
            with open(keystore_file, "r", encoding="utf-8") as f:
                store = json.load(f)
            if provider_clean in store:
                del store[provider_clean]
                with open(keystore_file, "w", encoding="utf-8") as f:
                    json.dump(store, f, indent=2)
                success = True
    except Exception:
        pass
    return success

def resolve_api_key(provider: str, explicit_key: str = "") -> str:
    """Resolve API key for a provider from explicit parameter, OS keyring, or system environment variables."""
    key = explicit_key.strip() if explicit_key else ""
    if key:
        return key

    provider_clean = (provider or "").lower().strip()
    # Check OS Keyring / encrypted keystore
    keyring_val = get_keyring_api_key(provider_clean)
    if keyring_val:
        return keyring_val

    # Check Environment Variables
    if provider_clean == "gemini":
        return os.environ.get("GEMINI_API_KEY", os.environ.get("GOOGLE_API_KEY", "")).strip()
    elif provider_clean == "openai":
        return os.environ.get("OPENAI_API_KEY", "").strip()
    return ""

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

