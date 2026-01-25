#!/bin/bash

# Configuration
REPO_USER="HeadyConnection"
REPO_NAME="HeadySystems"
REPO_URL="git@github.com:${REPO_USER}/${REPO_NAME}.git"
INSTALL_DIR="$HOME/${REPO_NAME}"
SSH_KEY_TYPE="ed25519"
SSH_KEY_PATH="$HOME/.ssh/id_${SSH_KEY_TYPE}"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting setup for ${REPO_NAME}...${NC}"

# ==============================================================================
# 1. Setup SSH Key for GitHub (Outgoing Passwordless Auth)
# ==============================================================================
echo -e "\n${YELLOW}[Step 1] Setting up SSH key for GitHub...${NC}"

if [ ! -f "$SSH_KEY_PATH" ]; then
    echo "Generating new SSH key ($SSH_KEY_TYPE)..."
    ssh-keygen -t $SSH_KEY_TYPE -C "setup_script_$(date +%Y%m%d)" -f "$SSH_KEY_PATH" -N ""
    echo -e "${GREEN}Key generated.${NC}"
else
    echo "SSH key already exists at $SSH_KEY_PATH. Skipping generation."
fi

# Ensure ssh-agent is running
eval "$(ssh-agent -s)" > /dev/null
ssh-add "$SSH_KEY_PATH" > /dev/null 2>&1

echo -e "\n${YELLOW}=== ACTION REQUIRED ===${NC}"
echo "Please copy the following public key and add it to your GitHub Account:"
echo "URL: https://github.com/settings/ssh/new"
echo "----------------------------------------------------------------------"
cat "${SSH_KEY_PATH}.pub"
echo "----------------------------------------------------------------------"
read -p "Press [Enter] once you have added the key to GitHub to continue..."

# Test connection
echo "Testing connection to GitHub..."
ssh -T -o StrictHostKeyChecking=no git@github.com &> /dev/null
if [ $? -eq 1 ]; then
    echo -e "${GREEN}Connection confirmed! (GitHub successfully authenticated you)${NC}"
else
    echo -e "${RED}Warning: Could not authenticate with GitHub. Cloning might fail.${NC}"
    read -p "Press [Enter] to continue anyway, or Ctrl+C to abort..."
fi

# ==============================================================================
# 2. Clone Repository
# ==============================================================================
echo -e "\n${YELLOW}[Step 2] Cloning repository...${NC}"

if [ -d "$INSTALL_DIR" ]; then
    echo "Directory $INSTALL_DIR already exists. Pulling latest changes..."
    cd "$INSTALL_DIR" && git pull
else
    git clone "$REPO_URL" "$INSTALL_DIR"
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to clone repository. Please check your SSH key settings above.${NC}"
        exit 1
    fi
fi

# ==============================================================================
# 3. Permissions & Group Assignments
# ==============================================================================
echo -e "\n${YELLOW}[Step 3] Setting permissions and ownership...${NC}"

# Set ownership to current user and their primary group
sudo chown -R $USER:$(id -gn) "$INSTALL_DIR"

# Set standard directory permissions (755) and file permissions (644)
find "$INSTALL_DIR" -type d -exec chmod 755 {} \;
find "$INSTALL_DIR" -type f -exec chmod 644 {} \;
# Make scripts executable if found
find "$INSTALL_DIR" -name "*.sh" -exec chmod +x {} \;

echo -e "${GREEN}Permissions updated.${NC}"

# ==============================================================================
# 4. Install Dependencies (Auto-Detect)
# ==============================================================================
echo -e "\n${YELLOW}[Step 4] Detecting and installing dependencies...${NC}"
cd "$INSTALL_DIR"

INSTALLED_SOMETHING=false

if [ -f "package.json" ]; then
    echo "Found package.json. Installing Node.js dependencies..."
    if command -v npm &> /dev/null; then
        npm install
        INSTALLED_SOMETHING=true
    else
        echo -e "${RED}Error: npm is not installed.${NC}"
    fi
fi

if [ -f "requirements.txt" ]; then
    echo "Found requirements.txt. Installing Python dependencies..."
    if command -v pip &> /dev/null; then
        pip install -r requirements.txt
        INSTALLED_SOMETHING=true
    elif command -v pip3 &> /dev/null; then
        pip3 install -r requirements.txt
        INSTALLED_SOMETHING=true
    else
        echo -e "${RED}Error: pip is not installed.${NC}"
    fi
fi

if [ -f "Gemfile" ]; then
    echo "Found Gemfile. Installing Ruby dependencies..."
    if command -v bundle &> /dev/null; then
        bundle install
        INSTALLED_SOMETHING=true
    else
        echo -e "${RED}Error: bundler is not installed.${NC}"
    fi
fi

if [ -f "composer.json" ]; then
    echo "Found composer.json. Installing PHP dependencies..."
    if command -v composer &> /dev/null; then
        composer install
        INSTALLED_SOMETHING=true
    else
        echo -e "${RED}Error: composer is not installed.${NC}"
    fi
fi

if [ -f "Makefile" ]; then
    echo "Found Makefile. Attempting to build..."
    make
    INSTALLED_SOMETHING=true
fi

if [ "$INSTALLED_SOMETHING" = false ]; then
    echo "No standard dependency files found (package.json, requirements.txt, etc.). Skipping."
else
    echo -e "${GREEN}Dependencies processed.${NC}"
fi

# ==============================================================================
# 5. Setup System for Incoming Passwordless SSH (Optional)
# ==============================================================================
echo -e "\n${YELLOW}[Step 5] Setting up system for INCOMING passwordless SSH login...${NC}"
echo "This allows you to SSH INTO this machine without a password using keys."

# 5a. Ensure authorized_keys exists and has correct permissions
mkdir -p "$HOME/.ssh"
chmod 700 "$HOME/.ssh"
touch "$HOME/.ssh/authorized_keys"
chmod 600 "$HOME/.ssh/authorized_keys"

# If the user has a public key they want to use to login TO this box, they need to add it.
# We will just ensure the current user's key is authorized (useful for testing localhost ssh)
if ! grep -q "$(cat $SSH_KEY_PATH.pub)" "$HOME/.ssh/authorized_keys"; then
    cat "$SSH_KEY_PATH.pub" >> "$HOME/.ssh/authorized_keys"
    echo "Added local public key to authorized_keys (allows 'ssh localhost' without password)."
fi

# 5b. Configure SSH Daemon (Requires Sudo)
read -p "Do you want to configure the system SSH daemon (sshd_config) to allow key-based auth? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Backing up sshd_config..."
    sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak

    echo "Configuring sshd..."
    # Enable PubkeyAuthentication
    sudo sed -i 's/^#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config
    sudo sed -i 's/^PubkeyAuthentication no/PubkeyAuthentication yes/' /etc/ssh/sshd_config
    
    # Ensure AuthorizedKeysFile is set
    # (Some systems default this correctly, but being explicit helps)
    if ! grep -q "^AuthorizedKeysFile" /etc/ssh/sshd_config; then
        echo "AuthorizedKeysFile      .ssh/authorized_keys .ssh/authorized_keys2" | sudo tee -a /etc/ssh/sshd_config
    fi

    echo "Restarting SSH service..."
    if command -v systemctl &> /dev/null; then
        sudo systemctl restart ssh || sudo systemctl restart sshd
    else
        sudo service ssh restart || sudo service sshd restart
    fi
    
    echo -e "${GREEN}System SSH configuration updated.${NC}"
else
    echo "Skipping system SSH daemon configuration."
fi

echo -e "\n${GREEN}=== Setup Complete ===${NC}"
