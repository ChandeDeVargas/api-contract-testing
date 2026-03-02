#!/bin/bash

echo "============================================"
echo "   NEWMAN INSTALLATION"
echo "============================================"
echo

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js not found!"
    echo
    echo "Please install Node.js first:"
    echo "  https://nodejs.org/"
    echo
    exit 1
fi

echo "[INFO] Node.js found"
node --version

echo
echo "[INFO] Installing Newman globally..."
npm install -g newman

echo
echo "[INFO] Installing Newman HTML reporter..."
npm install -g newman-reporter-htmlextra

echo
echo "============================================"
echo "   INSTALLATION COMPLETE"
echo "============================================"
echo
echo "Newman installed successfully!"
echo
echo "To verify: newman --version"
echo

chmod +x install_newman.sh