#!/bin/bash
# setup_session.sh: Initialize workspace environment at the start of a session.

set -e

echo "==========================================="
echo "  Initializing Workspace Session Environment"
echo "==========================================="

# 1. Sync dependencies with uv
if command -v uv &> /dev/null; then
    echo "[1/2] Syncing python dependencies with uv..."
    uv sync
else
    echo "[1/2] Warning: 'uv' command not found. Skipping dependency sync."
fi

# 2. Update agent skills
echo "[2/2] Fetching latest agent skill updates..."
if command -v npx &> /dev/null; then
    npx skills update -p -y || echo "Warning: skills update encountered an issue, skipping."
else
    echo "Warning: 'npx' command not found. Skipping skill updates."
fi

echo "==========================================="
echo "  Initialization Complete!"
echo "==========================================="
