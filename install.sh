#!/bin/bash

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Instalando Lazarus Downloader ===${NC}"

# 1. Definir diretórios
BIN_DIR="$HOME/.local/bin"
ACTION_DIR="$HOME/.local/share/nemo/actions"
ICON_DIR="$HOME/.local/share/icons"

# 2. Criar diretórios
mkdir -p "$BIN_DIR"
mkdir -p "$ACTION_DIR"
mkdir -p "$ICON_DIR"

# 3. Verificar dependências
echo -e "${BLUE}[+] Verificando dependências Python...${NC}"
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
else
    echo "Erro: pip3 não encontrado. Instale o python3-pip."
    exit 1
fi

# 4. Instalar Script Python
echo -e "${BLUE}[+] Instalando script...${NC}"
cp src/nemo_downloader_ui_ressurector.py "$BIN_DIR/nemo_downloader_ui_ressurector.py"
chmod +x "$BIN_DIR/nemo_downloader_ui_ressurector.py"

# 5. Instalar Ícone (NOVO)
# O sistema procura pelo nome do arquivo na pasta ~/.local/share/icons
echo -e "${BLUE}[+] Instalando ícone...${NC}"
if [ -f "assets/icon.png" ]; then
    cp assets/icon.png "$ICON_DIR/lazarus-downloader.png"
else
    echo "Aviso: assets/icon.png não encontrado. O ícone padrão será usado."
fi

# 6. Instalar Nemo Action
echo -e "${BLUE}[+] Configurando Nemo Action...${NC}"
cp nemo_action/wget_here_ressurector.nemo_action "$ACTION_DIR/"

# 7. Finalizar
echo -e "${GREEN}=== Instalação Concluída! ===${NC}"
echo "Se o ícone não aparecer imediatamente, execute: nemo -q"
