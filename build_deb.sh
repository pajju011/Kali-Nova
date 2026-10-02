#!/usr/bin/env bash
# ==============================================================================
# Kali-Nova: Debian (.deb) Package Builder for Kali Linux
# ==============================================================================

set -e

# Package details
PKG_NAME="kalinova"
PKG_VERSION="1.0.0"
PKG_ARCH="all"
DEB_NAME="${PKG_NAME}_${PKG_VERSION}_${PKG_ARCH}.deb"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="${SCRIPT_DIR}/build_pkg"
PKG_ROOT="${BUILD_DIR}/${PKG_NAME}_${PKG_VERSION}_${PKG_ARCH}"

echo "======================================================"
echo "   🛡️ Building Kali Linux Package (.deb) for Kali-Nova"
echo "======================================================"

# Clean up previous build
rm -rf "${BUILD_DIR}"
mkdir -p "${PKG_ROOT}/DEBIAN"
mkdir -p "${PKG_ROOT}/usr/bin"
mkdir -p "${PKG_ROOT}/usr/share/kalinova"
mkdir -p "${PKG_ROOT}/usr/share/applications"
mkdir -p "${PKG_ROOT}/usr/share/icons/hicolor/scalable/apps"

# 1. Create DEBIAN/control
cat << 'EOF' > "${PKG_ROOT}/DEBIAN/control"
Package: kalinova
Version: 1.0.0
Section: utils
Priority: optional
Architecture: all
Maintainer: Prajwal R Poojary <prajwal.r.poojary11@gmail.com>
Depends: python3, python3-pyqt6, python3-pyqt6.qtsvg, python3-reportlab, python3-pil, python3-pygments
Recommends: nmap, sqlmap, nikto, hydra, gobuster, wifite, john, hashcat, wireshark
Description: Kali-Nova Security Control Center
 Modern PyQt6 desktop control center for ethical security workflows,
 reconnaissance, automated testing, and AI-assisted penetration testing on Kali Linux.
EOF

# 2. Create DEBIAN/postinst
cat << 'EOF' > "${PKG_ROOT}/DEBIAN/postinst"
#!/bin/sh
set -e
if [ -x /usr/bin/update-desktop-database ]; then
    update-desktop-database /usr/share/applications >/dev/null 2>&1 || true
fi
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    gtk-update-icon-cache -f -t /usr/share/icons/hicolor >/dev/null 2>&1 || true
fi
exit 0
EOF
chmod 755 "${PKG_ROOT}/DEBIAN/postinst"

# 3. Create DEBIAN/postrm
cat << 'EOF' > "${PKG_ROOT}/DEBIAN/postrm"
#!/bin/sh
set -e
if [ -x /usr/bin/update-desktop-database ]; then
    update-desktop-database /usr/share/applications >/dev/null 2>&1 || true
fi
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    gtk-update-icon-cache -f -t /usr/share/icons/hicolor >/dev/null 2>&1 || true
fi
exit 0
EOF
chmod 755 "${PKG_ROOT}/DEBIAN/postrm"

# 4. Create executable launcher /usr/bin/kalinova
cat << 'EOF' > "${PKG_ROOT}/usr/bin/kalinova"
#!/bin/sh
exec python3 /usr/share/kalinova/main.py "$@"
EOF
chmod 755 "${PKG_ROOT}/usr/bin/kalinova"

# 5. Copy desktop entry
if [ -f "${SCRIPT_DIR}/kalinova.desktop" ]; then
    cp "${SCRIPT_DIR}/kalinova.desktop" "${PKG_ROOT}/usr/share/applications/kalinova.desktop"
fi

# 6. Copy app icon
if [ -f "${SCRIPT_DIR}/kalinova/resources/icons/kalinova.svg" ]; then
    cp "${SCRIPT_DIR}/kalinova/resources/icons/kalinova.svg" "${PKG_ROOT}/usr/share/icons/hicolor/scalable/apps/kalinova.svg"
fi

# 7. Copy application source files
echo "[*] Copying Kali-Nova source files..."
cp -r "${SCRIPT_DIR}/kalinova/"* "${PKG_ROOT}/usr/share/kalinova/"

# Clean up pycache, venv, and temporary build files from payload
find "${PKG_ROOT}/usr/share/kalinova" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "${PKG_ROOT}/usr/share/kalinova" -type d -name "venv" -exec rm -rf {} + 2>/dev/null || true
find "${PKG_ROOT}/usr/share/kalinova" -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
find "${PKG_ROOT}/usr/share/kalinova" -name "*.pyc" -delete 2>/dev/null || true

# 8. Build Debian package
echo "[*] Building Debian package..."
dpkg-deb --build --root-owner-group "${PKG_ROOT}" "${SCRIPT_DIR}/${DEB_NAME}"

# Clean up temporary build files
rm -rf "${BUILD_DIR}"

echo ""
echo "======================================================"
echo " ✅ Successfully created: ${DEB_NAME}"
echo "======================================================"
echo "To install on Kali Linux:"
echo "   sudo apt install ./${DEB_NAME}"
echo "Or using dpkg:"
echo "   sudo dpkg -i ${DEB_NAME}"
echo "   sudo apt-get install -f"
echo "======================================================"
