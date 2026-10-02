#!/usr/bin/env bash
# ==============================================================================
# Kali-Nova: Automated Installer & Environment Setup for Kali Linux
# ==============================================================================

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}======================================================${NC}"
echo -e "${GREEN}   🛡️  KALI-NOVA: Security Control Center Setup       ${NC}"
echo -e "${CYAN}======================================================${NC}"

# 1. Check Root Privileges for System Package Installation
if [ "$EUID" -ne 0 ]; then
    echo -e "${YELLOW}[!] Note: Running without root. Sudo will be prompted for apt packages.${NC}"
    SUDO="sudo"
else
    SUDO=""
fi

# 2. Install System & Python Dependencies on Kali Linux
echo -e "\n${CYAN}[1/4] Installing required system and Python packages...${NC}"
$SUDO apt update -y
$SUDO apt install -y python3 python3-pip python3-pyqt6 python3-reportlab python3-pytest polkit-1-auth-agent policykit-1-gnome

# 3. Check and extract rockyou wordlist if needed
echo -e "\n${CYAN}[2/4] Checking standard Kali security wordlists...${NC}"
if [ -f "/usr/share/wordlists/rockyou.txt.gz" ] && [ ! -f "/usr/share/wordlists/rockyou.txt" ]; then
    echo -e "${YELLOW}[*] Decompressing /usr/share/wordlists/rockyou.txt.gz...${NC}"
    $SUDO gunzip -k /usr/share/wordlists/rockyou.txt.gz
    echo -e "${GREEN}[+] rockyou.txt is ready.${NC}"
else
    echo -e "${GREEN}[+] Wordlists already verified.${NC}"
fi

# 4. Install application files to /usr/share/kalinova and create /usr/bin/kalinova launcher
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo -e "\n${CYAN}[3/4] Installing application files and launcher...${NC}"

$SUDO mkdir -p /usr/share/kalinova
$SUDO cp -r "$APP_DIR/kalinova/"* /usr/share/kalinova/

cat << 'EOF' | $SUDO tee /usr/bin/kalinova > /dev/null
#!/usr/bin/env bash
cd /usr/share/kalinova
exec python3 main.py "$@"
EOF

$SUDO chmod +x /usr/bin/kalinova

# 5. Install Desktop Entry and Icons for Kali Applications Menu
echo -e "\n${CYAN}[4/4] Registering Desktop Application in Kali Linux menu...${NC}"
if [ -f "$APP_DIR/kalinova.desktop" ]; then
    $SUDO cp "$APP_DIR/kalinova.desktop" /usr/share/applications/kalinova.desktop
fi
if [ -f "$APP_DIR/kalinova/resources/icons/kalinova.svg" ]; then
    $SUDO mkdir -p /usr/share/icons/hicolor/scalable/apps
    $SUDO cp "$APP_DIR/kalinova/resources/icons/kalinova.svg" /usr/share/icons/hicolor/scalable/apps/kalinova.svg
fi
$SUDO update-desktop-database /usr/share/applications/ 2>/dev/null || true
$SUDO gtk-update-icon-cache -f -t /usr/share/icons/hicolor 2>/dev/null || true
echo -e "${GREEN}[+] Registered in Kali Linux Applications Menu.${NC}"

echo -e "\n${GREEN}======================================================${NC}"
echo -e "${GREEN} ✅  Kali-Nova setup complete!                         ${NC}"
echo -e "${CYAN} Launch Kali-Nova from terminal with:${NC}  kalinova"
echo -e "${CYAN} Or launch directly via:${NC}              python3 $APP_DIR/kalinova/main.py"
echo -e "${GREEN}======================================================${NC}\n"
