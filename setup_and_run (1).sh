#!/bin/bash

# Configuration
DEFAULT_REPO="https://github.com/HeadyConnection/HeadySystems.git"
DIR_NAME="HeadySystems"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}   HeadySystems Setup & Execution        ${NC}"
echo -e "${BLUE}=========================================${NC}"

# 1. Install Dependencies
echo -e "\n${YELLOW}[1/5] Checking system dependencies...${NC}"

# Install Cloudflared (Non-interactive)
if ! command -v cloudflared &> /dev/null; then
    echo -e "${YELLOW}Installing cloudflared...${NC}"
    wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
    dpkg -i cloudflared-linux-amd64.deb >/dev/null 2>&1
    rm cloudflared-linux-amd64.deb
    echo -e "${GREEN}cloudflared installed.${NC}"
else
    echo -e "${GREEN}cloudflared is already installed.${NC}"
fi

# 2. Repository Setup
echo -e "\n${YELLOW}[2/5] Checking Repository...${NC}"
if [ -d "$DIR_NAME" ]; then
    if [ -d "$DIR_NAME/.git" ]; then
        echo -e "Git repo detected. Pulling latest changes..."
        cd "$DIR_NAME"
        git pull
    else
        echo -e "${YELLOW}Directory exists but is not a git repo. Skipping git pull to preserve local build.${NC}"
        cd "$DIR_NAME"
    fi
else
    echo -e "Cloning repository..."
    git clone "$DEFAULT_REPO" "$DIR_NAME"
    cd "$DIR_NAME"
fi

# 3. Python Environment
echo -e "\n${YELLOW}[3/5] Setting up Python Environment...${NC}"
pip install --upgrade pip >/dev/null 2>&1
pip install fastapi uvicorn psutil requests >/dev/null 2>&1
echo -e "${GREEN}Dependencies installed.${NC}"

# 4. Configuration Check
echo -e "\n${YELLOW}[4/5] Checking Configuration...${NC}"
if [ -f "heady_project/config/projects.json" ]; then
    echo -e "${GREEN}Configuration found.${NC}"
else
    echo -e "${RED}Warning: projects.json not found.${NC}"
fi

# 5. Launch Application
echo -e "\n${YELLOW}[5/5] Launching Heady API...${NC}"
if [ -f "heady_project/src/admin_console.py" ]; then
    echo -e "${GREEN}Starting Admin Console (serve_api)...${NC}"
    # Run in background with timeout for demo purposes
    python3 heady_project/src/admin_console.py --action serve_api &
    SERVER_PID=$!
    sleep 5
    
    # Check health
    echo -e "\nChecking API Health..."
    curl -s http://127.0.0.1:8000/health || echo "API Check Failed"
    
    echo -e "\n${GREEN}Server running with PID $SERVER_PID.${NC}"
    echo -e "Shutting down for demo completion..."
    kill $SERVER_PID
else
    echo -e "${RED}Error: admin_console.py not found.${NC}"
fi

echo -e "\n${BLUE}=== Done ===${NC}"
