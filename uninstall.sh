#!/bin/bash

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${RED}=== Uninstalling Lazarus Downloader ===${NC}"

BIN_DIR="$HOME/.local/bin"
ACTION_DIR="$HOME/.local/share/nemo/actions"

# Remove script
if [ -f "$BIN_DIR/nemo_downloader_ui_ressurector.py" ]; then
    rm -f "$BIN_DIR/nemo_downloader_ui_ressurector.py"
    echo -e "${GREEN}✓ Removed script${NC}"
else
    echo -e "${BLUE}ℹ Script not found${NC}"
fi

# Remove Nemo action
if [ -f "$ACTION_DIR/lazarus_download.nemo_action" ]; then
    rm -f "$ACTION_DIR/lazarus_download.nemo_action"
    echo -e "${GREEN}✓ Removed Nemo action${NC}"
else
    echo -e "${BLUE}ℹ Nemo action not found${NC}"
fi

echo ""
echo -e "${GREEN}Uninstall complete.${NC}"
echo ""
echo -e "${BLUE}Optional cleanup:${NC}"
echo "  Remove Python dependencies (if not used elsewhere):"
echo "    pip3 uninstall PySide6 urllib3"
echo ""
echo "  Remove PATH configuration from ~/.bashrc:"
echo "    Edit ~/.bashrc and remove the line:"
echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
echo ""
echo "  Restart Nemo:"
echo "    nemo -q"
