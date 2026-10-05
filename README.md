# Kali-Nova

[![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-blue.svg)](https://www.kali.org/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![GUI Framework](https://img.shields.io/badge/GUI-PyQt6-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](file:///c:/Users/ASUS/Desktop/Kali-Nova/LICENSE)

**Kali-Nova** is an advanced PyQt6 desktop control center designed for ethical security testing and penetration testing workflows on **Kali Linux**.

It transforms raw command-line security tools into an integrated, interactive workspace featuring real-time telemetry, AI Copilot diagnostic remediation, dynamic radar network topology visualization, automated risk scoring, SQLite session history, and professional PDF/HTML report exports.

The application source code, modules, tests, and architectural guidelines are located in the [`kalinova/`](file:///c:/Users/ASUS/Desktop/Kali-Nova/kalinova) folder.

For comprehensive developer documentation and AI collaboration protocols, see:
👉 **[kalinova/README.md](file:///c:/Users/ASUS/Desktop/Kali-Nova/kalinova/README.md)**

---

## ⚡ Quick Start & Installation

Choose your preferred installation method:

### 1. One-Line Automated Installer (Recommended for Kali Linux)

Run the automated installer script to fetch dependencies, register system shortcuts, and install the global `kalinova` command:

```bash
curl -sSL https://raw.githubusercontent.com/pajju011/Kali-Nova/main/install_kali.sh | bash
```

*Or via `wget`:*

```bash
wget -qO- https://raw.githubusercontent.com/pajju011/Kali-Nova/main/install_kali.sh | bash
```

---

### 2. Install via Official APT Repository (Kali Linux)

Add the official Kali-Nova APT repository hosted on GitHub Pages:

```bash
# 1. Add Kali-Nova repository GPG signing key
curl -fsSL https://pajju011.github.io/Kali-Nova/kalinova-archive-keyring.asc | sudo tee /etc/apt/trusted.gpg.d/kalinova.asc > /dev/null

# 2. Add APT repository source list
echo "deb https://pajju011.github.io/Kali-Nova/ stable main" | sudo tee /etc/apt/sources.list.d/kalinova.list

# 3. Update packages and install Kali-Nova
sudo apt update
sudo apt install -y kalinova
```

---

### 3. Build & Install Debian (.deb) Package

You can build and install the Debian package directly from source:

```bash
git clone https://github.com/pajju011/Kali-Nova.git
cd Kali-Nova
chmod +x build_deb.sh
./build_deb.sh --install
```

---

### 4. Running Kali-Nova

Once installed, launch Kali-Nova from any terminal:

```bash
kalinova
```

Or open **Kali-Nova** from your desktop application menu under **Security** / **Penetration Testing**.

---

### 5. Windows Quick Launch

For testing on Windows systems:

- Double-click [`run.bat`](file:///c:/Users/ASUS/Desktop/Kali-Nova/run.bat), or
- Execute via PowerShell:
  ```powershell
  .\run_windows.ps1
  ```

---

### 6. Manual Setup / Development Environment

If you are developing or testing locally within a Python virtual environment:

```bash
# Clone the repository
git clone https://github.com/pajju011/Kali-Nova.git
cd Kali-Nova/kalinova

# Create & activate a virtual environment
python3 -m venv venv
source venv/bin/activate       # On Linux/macOS
# or: venv\Scripts\activate    # On Windows

# Install required dependencies
pip install -r requirements.txt

# Run the test suite
pytest tests/

# Launch Kali-Nova
python3 main.py
```

---

## 🛡️ Key Features

- **Integrated Security Modules**: Dedicated GUI workflows for Nmap, Whois, theHarvester, Nikto, SQLmap, Gobuster, Hydra, John the Ripper, Netcat, Wireshark, Wifite, Wash, Reaver, SSLScan, SSLyze, and TLSSLed.
- **Live Output Streaming & Event Detection**: Asynchronous subprocess execution with color-coded syntax output and automated security signal triggers.
- **Dynamic Threat Intelligence**: Automated risk calculator evaluating open port surfaces and vulnerability alerts.
- **AI Copilot Diagnostics**: Real-time CVSS scoring analysis and tailored remediation code snippets (Python & Node.js).
- **Network Topology Visualizer**: Animated 20 FPS radar sweeps rendering discovered network nodes and port states.
- **Persistent Database & Reporting**: SQLite storage (`kalinova.db`) tracking scan histories with one-click PDF and HTML audit reports.

---

## 👥 Authors & Contributors

- **Shravyashree M S**
- **Pooja**
- **Shreyank**
- **Prajwal R Poojary**

---

## 📜 License

Copyright (C) 2026 Shravyashree M S, Pooja, Shreyank, Prajwal R Poojary.

This project is licensed under the [GNU General Public License v3.0](file:///c:/Users/ASUS/Desktop/Kali-Nova/LICENSE) - see the [LICENSE](file:///c:/Users/ASUS/Desktop/Kali-Nova/LICENSE) file for details.


