#!/bin/sh
# Copyright (c) 2026 Uno Kim / AMEVA Foundation. All rights reserved.
# SPDX-License-Identifier: Apache-2.0 OR Commercial-License
set -e
echo "================================================================="
echo "   AMV-Playwright Automated Installer"
echo "================================================================="
if [ -z "${PREFIX:-}" ] && [ ! -d "/data/data/com.termux" ]; then
    echo "[*] Non-Termux environment detected. Installing standard Playwright..."
    python3 -m pip install setuptools --quiet
    python3 -m pip install amv-playwright --quiet
    amv-playwright-install
    amv-playwright-doctor
    echo "[+] Installation complete."
    exit 0
fi
ARCH=$(uname -m)
echo "[*] Termux environment detected (Architecture: ${ARCH})"
if [ "${ARCH}" != "aarch64" ] && [ "${ARCH}" != "arm64" ]; then
    echo "[!] Warning: Architecture is not aarch64. Running in compatibility mode."
fi
echo "[1/4] Installing Termux system packages..."
pkg update -y || apt update -y || true
pkg install -y chromium nodejs python python-greenlet procps termux-api || apt-get install -y --fix-missing chromium nodejs python python-greenlet procps termux-api
echo "[2/4] Installing Python base dependencies..."
python3 -m pip install setuptools --quiet
python3 -m pip install pyee typing-extensions amv-playwright --prefer-binary --quiet
echo "[3/4] Installing Playwright wheel and applying core patch..."
amv-playwright-install
echo "[4/4] Verifying system readiness..."
amv-playwright-doctor
echo "================================================================="
echo "   AMV-Playwright Installation Completed Successfully"
echo "================================================================="
