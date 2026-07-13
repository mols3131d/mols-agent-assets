#!/bin/bash
# setup_session.sh: Initialize workspace environment at the start of a session.

set -e

echo "==========================================="
echo "  Initializing Workspace Session Environment"
echo "==========================================="

# 1. Sync dependencies with uv
if command -v uv &> /dev/null; then
    echo "[1/3] Syncing python dependencies with uv..."
    uv sync
else
    echo "[1/3] Warning: 'uv' command not found. Skipping dependency sync."
fi

# 2. Synchronize Lefthook Git hooks
if command -v uv &> /dev/null; then
    echo "[2/3] Registering Git hooks via lefthook..."
    uv run lefthook install
else
    echo "[2/3] Warning: 'uv' command not found. Skipping lefthook installation."
fi

# 3. Update agent skills
echo "[3/3] Fetching latest agent skill updates..."
if command -v npx &> /dev/null; then
    npx skills update -p -y || echo "Warning: skills update encountered an issue, skipping."
else
    echo "Warning: 'npx' command not found. Skipping skill updates."
fi

echo "==========================================="
echo "  Initialization Complete!"
echo "==========================================="
