#!/bin/bash
# Heady Golden Master Deployment Script
set -e

echo ">>> Initiating Heady Golden Master Protocol..."

if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is missing."
    exit 1
fi

if [ -f "Heady_Golden_Master_Builder_v13.py" ]; then
    echo "[1/3] Executing Builder..."
    python3 Heady_Golden_Master_Builder_v13.py
fi

if [ ! -d ".git" ]; then
    git init
    echo "[2/3] Initialized git repository."
fi

if [ ! -f ".gitattributes" ]; then
    echo "*.wav filter=lfs diff=lfs merge=lfs -text" >.gitattributes
    echo "*.mp3 filter=lfs diff=lfs merge=lfs -text" >>.gitattributes
    echo "*.mid filter=lfs diff=lfs merge=lfs -text" >>.gitattributes
fi

git add .
if git diff --staged --quiet; then
    echo "No changes detected."
else
    git commit -m "Heady Golden Master v13: Auto-generated update"
    echo "[3/3] Committed baseline."
fi
