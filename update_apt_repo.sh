#!/usr/bin/env bash
# ==============================================================================
# Kali-Nova: Automated APT Repository Update Script
# Builds the latest .deb, updates Packages and Release, and signs with GPG
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APT_DIR="${SCRIPT_DIR}/apt-repo"
POOL_DIR="${APT_DIR}/pool/main/k/kalinova"
DISTS_DIR="${APT_DIR}/dists/stable"
BINARY_DIR="${DISTS_DIR}/main/binary-all"

echo "======================================================"
echo "   🛡️ Kali-Nova: APT Repository Updater              "
echo "======================================================"

# 1. Ensure build dependencies exist
if ! command -v dpkg-scanpackages >/dev/null 2>&1; then
    echo "[!] dpkg-scanpackages not found. Installing dpkg-dev..."
    if [ "$EUID" -eq 0 ]; then
        apt update && apt install -y dpkg-dev
    else
        sudo apt update && sudo apt install -y dpkg-dev
    fi
fi

# 2. Build the latest deb package
echo "[*] Building latest Debian package..."
"${SCRIPT_DIR}/build_deb.sh"

# Extract package filename and version from build_deb.sh
PKG_VERSION="$(grep -m1 '^PKG_VERSION=' "${SCRIPT_DIR}/build_deb.sh" | cut -d'"' -f2)"
DEB_NAME="kalinova_${PKG_VERSION}_all.deb"

if [ ! -f "${SCRIPT_DIR}/${DEB_NAME}" ]; then
    echo "[!] Error: ${DEB_NAME} was not found after build."
    exit 1
fi

# 3. Copy new package to pool
mkdir -p "${POOL_DIR}"
mkdir -p "${BINARY_DIR}"
cp "${SCRIPT_DIR}/${DEB_NAME}" "${POOL_DIR}/"
echo "[+] Copied ${DEB_NAME} to ${POOL_DIR}/"

# 4. Generate Packages and Packages.gz
echo "[*] Updating APT package index..."
cd "${APT_DIR}"
dpkg-scanpackages --arch all pool/ > "${BINARY_DIR}/Packages"
gzip -k -f "${BINARY_DIR}/Packages"

# 5. Generate Release file with correct checksums
echo "[*] Generating Release manifest..."
cd "${DISTS_DIR}"

cat << EOF > Release
Architectures: amd64 all
Codename: stable
Components: main
Date: $(date -Ru)
Description: Kali-Nova APT Repository
Label: Kali-Nova
Origin: Kali-Nova
Suite: stable
MD5Sum:
 $(md5sum main/binary-all/Packages | awk '{print $1}') $(wc -c < main/binary-all/Packages | awk '{print $1}') main/binary-all/Packages
 $(md5sum main/binary-all/Packages.gz | awk '{print $1}') $(wc -c < main/binary-all/Packages.gz | awk '{print $1}') main/binary-all/Packages.gz
SHA1:
 $(sha1sum main/binary-all/Packages | awk '{print $1}') $(wc -c < main/binary-all/Packages | awk '{print $1}') main/binary-all/Packages
 $(sha1sum main/binary-all/Packages.gz | awk '{print $1}') $(wc -c < main/binary-all/Packages.gz | awk '{print $1}') main/binary-all/Packages.gz
SHA256:
 $(sha256sum main/binary-all/Packages | awk '{print $1}') $(wc -c < main/binary-all/Packages | awk '{print $1}') main/binary-all/Packages
 $(sha256sum main/binary-all/Packages.gz | awk '{print $1}') $(wc -c < main/binary-all/Packages.gz | awk '{print $1}') main/binary-all/Packages.gz
SHA512:
 $(sha512sum main/binary-all/Packages | awk '{print $1}') $(wc -c < main/binary-all/Packages | awk '{print $1}') main/binary-all/Packages
 $(sha512sum main/binary-all/Packages.gz | awk '{print $1}') $(wc -c < main/binary-all/Packages.gz | awk '{print $1}') main/binary-all/Packages.gz
EOF

# 6. Sign Release if GPG key is present
GPG_KEY_ID="apt@kalinova.dev"
if gpg --list-secret-keys "$GPG_KEY_ID" >/dev/null 2>&1; then
    echo "[*] Signing Release file with GPG key: $GPG_KEY_ID..."
    rm -f Release.gpg InRelease
    gpg --default-key "$GPG_KEY_ID" -abs -o Release.gpg Release
    gpg --default-key "$GPG_KEY_ID" --clearsign -o InRelease Release
    echo "[+] Generated InRelease and Release.gpg"
else
    echo "[!] Note: Secret key for $GPG_KEY_ID not found in keyring. InRelease was not updated."
    echo "    To sign, run on the machine containing your private GPG key:"
    echo "    gpg --default-key apt@kalinova.dev --clearsign -o InRelease Release"
fi

echo ""
echo "======================================================"
echo " ✅ APT Repository successfully updated to v${PKG_VERSION}!"
echo " Commit and push apt-repo to publish via GitHub Pages:"
echo "    git add apt-repo/ && git commit -m 'chore: update apt repo to v${PKG_VERSION}' && git push"
echo "======================================================"
