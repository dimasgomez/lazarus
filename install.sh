#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Installing Lazarus Downloader ===${NC}"

# 1. Define paths (Local user installation)
BIN_DIR="$HOME/.local/bin"
ACTION_DIR="$HOME/.local/share/nemo/actions"

# 2. Create directories if needed
mkdir -p "$BIN_DIR"
mkdir -p "$ACTION_DIR"

# 3. Check Python dependencies
echo -e "${BLUE}[+] Checking Python dependencies...${NC}"
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
else
    echo "Error: pip3 not found. Please install python3-pip."
    exit 1
fi

# 4. Copy main script
echo -e "${BLUE}[+] Installing Python script to $BIN_DIR...${NC}"
cp src/nemo_downloader_ui_ressurector.py "$BIN_DIR/nemo_downloader_ui_ressurector.py"
chmod +x "$BIN_DIR/nemo_downloader_ui_ressurector.py"

# 5. Copy Nemo Action
echo -e "${BLUE}[+] Configuring Nemo Action...${NC}"
cp nemo_action/wget_here_ressurector.nemo_action "$ACTION_DIR/"

# 6. Finish
echo -e "${GREEN}=== Installation Complete! ===${NC}"
echo "Is the script accessible globally? $(command -v nemo_downloader_ui_ressurector.py >/dev/null 2>&1 && echo 'Yes' || echo 'You might need to restart your session')"
echo "Now simply right-click any folder in Nemo -> 'Download URL here (Lazarus)'"
