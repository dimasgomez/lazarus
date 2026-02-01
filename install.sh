#!/bin/bash

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Instalando Lazarus Downloader ===${NC}"

# 1. Definir diretórios (instalação local do usuário)
BIN_DIR="$HOME/.local/bin"
ACTION_DIR="$HOME/.local/share/nemo/actions"
ICON_DIR="$HOME/.local/share/icons"

# 2. Criar diretórios se necessário
echo -e "${BLUE}[+] Criando diretórios...${NC}"
mkdir -p "$BIN_DIR"
mkdir -p "$ACTION_DIR"
mkdir -p "$ICON_DIR"

# 3. Verificar versão do Python
echo -e "${BLUE}[+] Verificando Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Erro: Python 3 não encontrado. Instale o python3.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
echo -e "${GREEN}✓ Python $PYTHON_VERSION detectado${NC}"

# 4. Verificar e instalar dependências Python
echo -e "${BLUE}[+] Verificando dependências Python...${NC}"
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}Erro: pip3 não encontrado. Instale o python3-pip.${NC}"
    exit 1
fi

pip3 install --user -r requirements.txt || {
    echo -e "${RED}Falha ao instalar dependências${NC}"
    exit 1
}
echo -e "${GREEN}✓ Dependências instaladas${NC}"

# 5. Instalar Script Python
echo -e "${BLUE}[+] Instalando script...${NC}"
if [ -f "src/nemo_downloader_ui_ressurector.py" ]; then
    cp src/nemo_downloader_ui_ressurector.py "$BIN_DIR/nemo_downloader_ui_ressurector.py"
    chmod +x "$BIN_DIR/nemo_downloader_ui_ressurector.py"
    echo -e "${GREEN}✓ Script instalado${NC}"
else
    echo -e "${RED}Erro: src/nemo_downloader_ui_ressurector.py não encontrado${NC}"
    exit 1
fi

# 6. Instalar Ícone
echo -e "${BLUE}[+] Instalando ícone...${NC}"
if [ -f "assets/icon.png" ]; then
    cp assets/icon.png "$ICON_DIR/lazarus-downloader.png"
    echo -e "${GREEN}✓ Ícone instalado${NC}"
else
    echo -e "${YELLOW}⚠ Aviso: assets/icon.png não encontrado. O ícone padrão será usado.${NC}"
fi

# 7. Instalar Nemo Action
echo -e "${BLUE}[+] Configurando Nemo Action...${NC}"
if [ -f "nemo_action/wget_here_lazarus.nemo_action" ]; then
    cp nemo_action/wget_here_lazarus.nemo_action "$ACTION_DIR/"
    echo -e "${GREEN}✓ Nemo Action configurado${NC}"
else
    echo -e "${RED}Erro: nemo_action/wget_here_lazarus.nemo_action não encontrado${NC}"
    exit 1
fi

# 8. Verificar se PATH inclui ~/.local/bin
echo -e "${BLUE}[+] Verificando PATH...${NC}"
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo -e "${YELLOW}[!] ~/.local/bin não está no seu PATH${NC}"
    echo -e "${BLUE}    Adicionando ao ~/.bashrc...${NC}"
    
    # Backup do bashrc
    cp ~/.bashrc ~/.bashrc.backup_lazarus_$(date +%Y%m%d_%H%M%S)
    
    # Adicionar ao PATH
    echo '' >> ~/.bashrc
    echo '# Adicionado pelo instalador do Lazarus Downloader' >> ~/.bashrc
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    
    echo -e "${GREEN}✓ PATH atualizado no ~/.bashrc${NC}"
    echo -e "${YELLOW}    Execute: ${NC}source ~/.bashrc"
    NEEDS_RELOAD=true
else
    echo -e "${GREEN}✓ PATH já configurado${NC}"
    NEEDS_RELOAD=false
fi

# 9. Finalizar
echo ""
echo -e "${GREEN}=== Instalação Concluída! ===${NC}"
echo ""

# Verificar acessibilidade do script
if command -v nemo_downloader_ui_ressurector.py >/dev/null 2>&1; then
    echo -e "${GREEN}✓ Script acessível globalmente${NC}"
else
    if [ "$NEEDS_RELOAD" = true ]; then
        echo -e "${YELLOW}⚠ Script instalado, mas não está no PATH ainda${NC}"
        echo -e "  Execute: ${BLUE}source ~/.bashrc${NC}"
        echo -e "  Ou reinicie o terminal"
    fi
fi

echo ""
echo -e "${BLUE}Como usar:${NC}"
echo "  1. Clique com o botão direito em qualquer pasta no Nemo"
echo "  2. Selecione 'Download with Lazarus'"
echo "  3. A interface de download abrirá automaticamente"
echo ""
echo -e "${BLUE}Ou pelo terminal:${NC}"
echo "  nemo_downloader_ui_ressurector.py [caminho_destino]"
echo ""
echo -e "${YELLOW}[!] Reinicie o Nemo para as mudanças terem efeito:${NC}"
echo "    nemo -q"
echo ""
