#!/usr/bin/env bash

set -e

REPO_URL="https://github.com/pajju011/Kali-Nova.git"
INSTALL_DIR="/usr/share/kalinova"
TEMP_DIR="/tmp/kalinova-install"

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}======================================================${NC}"
echo -e "${GREEN}       KALI-NOVA INSTALLER${NC}"
echo -e "${CYAN}======================================================${NC}"

# ------------------------------------------------------
# 1. Check sudo
# ------------------------------------------------------

if [ "$EUID" -eq 0 ]; then
    SUDO=""
else
    SUDO="sudo"
fi

# ------------------------------------------------------
# 2. Check Kali Linux
# ------------------------------------------------------

if [ ! -f /etc/os-release ]; then
    echo -e "${RED}[!] Cannot determine operating system.${NC}"
    exit 1
fi

. /etc/os-release

if [ "$ID" != "kali" ]; then
    echo -e "${YELLOW}[!] Kali-Nova is designed for Kali Linux.${NC}"
    echo -e "${YELLOW}[!] Detected OS: ${PRETTY_NAME}${NC}"
    exit 1
fi

echo -e "${GREEN}[+] Kali Linux detected.${NC}"

# ------------------------------------------------------
# 3. Install required packages
# ------------------------------------------------------

echo
echo -e "${CYAN}[1/5] Installing dependencies...${NC}"
# ------------------------------------------------------
$SUDO apt install -y \
    git \
    python3 \
    python3-pip \
    python3-pyqt6 \
    python3-pyqt6.qtsvg \
    python3-reportlab \
    python3-pil \
    python3-pygments \
    python3-pytest \
    polkitd \
    pkexec
# ------------------------------------------------------

echo
echo -e "${CYAN}[2/5] Downloading Kali-Nova...${NC}"

rm -rf "$TEMP_DIR"

git clone --depth 1 "$REPO_URL" "$TEMP_DIR"

echo -e "${GREEN}[+] Kali-Nova downloaded.${NC}"

# ------------------------------------------------------
# 5. Check application files
# ------------------------------------------------------

echo
echo -e "${CYAN}[3/5] Checking application files...${NC}"

if [ ! -f "$TEMP_DIR/kalinova/main.py" ]; then
    echo -e "${RED}[!] kalinova/main.py not found.${NC}"
    rm -rf "$TEMP_DIR"
    exit 1
fi

if [ ! -f "$TEMP_DIR/kalinova.desktop" ]; then
    echo -e "${RED}[!] kalinova.desktop not found.${NC}"
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo -e "${GREEN}[+] Application files verified.${NC}"

# ------------------------------------------------------
# 6. Install application
# ------------------------------------------------------

echo
echo -e "${CYAN}[4/5] Installing Kali-Nova...${NC}"

$SUDO rm -rf "$INSTALL_DIR"
$SUDO mkdir -p "$INSTALL_DIR"

$SUDO cp -r "$TEMP_DIR/kalinova/"* "$INSTALL_DIR/"

# ------------------------------------------------------
# 7. Create global command
# ------------------------------------------------------

$SUDO tee /usr/bin/kalinova > /dev/null <<'EOF'
#!/usr/bin/env bash

cd /usr/share/kalinova
exec python3 main.py "$@"
EOF

$SUDO chmod +x /usr/bin/kalinova

# ------------------------------------------------------
# 8. Install desktop entry
# ------------------------------------------------------

$SUDO cp \
    "$TEMP_DIR/kalinova.desktop" \
    /usr/share/applications/kalinova.desktop

# ------------------------------------------------------
# 9. Install icon
# ------------------------------------------------------

if [ -f "$TEMP_DIR/kalinova/resources/icons/kalinova.svg" ]; then

    $SUDO mkdir -p \
        /usr/share/icons/hicolor/scalable/apps

    $SUDO cp \
        "$TEMP_DIR/kalinova/resources/icons/kalinova.svg" \
        /usr/share/icons/hicolor/scalable/apps/kalinova.svg

fi

# ------------------------------------------------------
# 10. Update application menu
# ------------------------------------------------------

$SUDO update-desktop-database \
    /usr/share/applications/ \
    2>/dev/null || true

$SUDO gtk-update-icon-cache \
    -f -t /usr/share/icons/hicolor \
    2>/dev/null || true

# ------------------------------------------------------
# 11. Cleanup
# ------------------------------------------------------

rm -rf "$TEMP_DIR"

# ------------------------------------------------------
# 12. Verify installation
# ------------------------------------------------------

echo
echo -e "${CYAN}[5/5] Verifying installation...${NC}"

if command -v kalinova >/dev/null 2>&1; then

    echo -e "${GREEN}[+] kalinova command installed.${NC}"

else

    echo -e "${RED}[!] kalinova command was not installed correctly.${NC}"
    exit 1

fi

if [ -f "/usr/share/applications/kalinova.desktop" ]; then

    echo -e "${GREEN}[+] Application menu entry installed.${NC}"

fi

echo
echo -e "${GREEN}======================================================${NC}"
echo -e "${GREEN}       KALI-NOVA INSTALLATION COMPLETE${NC}"
echo -e "${GREEN}======================================================${NC}"

echo
echo -e "${CYAN}Launch Kali-Nova:${NC}"
echo
echo "    kalinova"
echo
echo -e "${CYAN}Application installed at:${NC}"
echo
echo "    /usr/share/kalinova"
echo
echo -e "${GREEN}Kali-Nova is ready.${NC}"
echo

