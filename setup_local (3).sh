#!/bin/bash

# Heady Systems Local Setup & Runner
# ----------------------------------
# Installs dependencies, configures environment, and launches the platform with tunneling.

set -e

echo "=== Heady Systems Local Setup ==="

# 1. Check Prerequisites
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found."
    exit 1
fi

# 2. Setup Virtual Environment
if [ ! -d "venv" ]; then
    echo "⚙️ Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# 3. Install Dependencies
echo "⚙️ Installing Python dependencies..."
pip install --upgrade pip
pip install fastapi uvicorn psutil requests

# 4. Check Cloudflared
if ! command -v cloudflared &> /dev/null; then
    echo "⚠️ 'cloudflared' not found. Tunneling will be disabled."
    echo "   To enable tunneling, install from: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation"
    HAS_CLOUDFLARED=false
else
    HAS_CLOUDFLARED=true
fi

# 5. Launch System
echo "
=== Launching Heady Platform ==="

# Function to cleanup background processes
cleanup() {
    echo "Shutting down..."
    kill $(jobs -p) 2>/dev/null
}
trap cleanup EXIT

# Start API Server
echo "⚡ Starting API Server (Background)..."
python3 heady_project/src/admin_console.py --action serve_api &
API_PID=$!

# Wait for server
sleep 5

# Start Tunnel
if [ "$HAS_CLOUDFLARED" = true ]; then
    echo "☁️ Starting Cloudflare Tunnel..."
    # Quick Tunnel (TryCloudflare)
    cloudflared tunnel --url http://localhost:8000 &
else
    echo "❌ Cloudflare Tunnel skipped."
    echo "   Local Access: http://localhost:8000/health"
fi

# Keep script running to maintain processes
wait
