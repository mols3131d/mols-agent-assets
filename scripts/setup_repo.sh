#!/bin/bash
# setup_repo.sh: Initial repository setup for first-time users.

set -e

echo "==========================================="
echo "  Setting Up Repository for the First Time"
echo "==========================================="

# 1. Install/Sync dependencies using uv
if command -v uv &> /dev/null; then
    echo "[1/3] Syncing python dependencies with uv..."
    uv sync
else
    echo "[1/3] Error: 'uv' command not found. Please install uv first (https://astral.sh/uv)."
    exit 1
fi

# 2. Install Lefthook Git hooks
echo "[2/3] Installing Git hooks via lefthook..."
uv run lefthook install

# 3. Perform initial skill update
echo "[3/3] Fetching initial agent skills..."
if command -v npx &> /dev/null; then
    npx skills update -p -y || echo "Warning: skills update encountered an issue."
else
    echo "Warning: 'npx' command not found. Skipping initial skill updates."
fi

echo "==========================================="
echo "  Setup Complete! You can now start coding."
echo "==========================================="
