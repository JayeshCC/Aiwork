#!/bin/bash

echo "=========================================="
echo "      AIWork Setup Script (Linux/Mac)"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "[*] Creating virtual environment..."
    python3 -m venv .venv
else
    echo "[*] Virtual environment already exists."
fi

# Activate and install dependencies
echo "[*] Activating virtual environment..."
source .venv/bin/activate

echo "[*] Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "      Setup Complete! "
echo "=========================================="
echo ""
echo "To start, run:"
echo "   source .venv/bin/activate"
echo "   python examples/quickstart.py"
echo ""
