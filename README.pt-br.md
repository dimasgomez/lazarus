# Lazarus Downloader for Anna's Archive (pt-br)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Linux](https://img.shields.io/badge/Linux-Mint%20%7C%20Nemo-green.svg)

Uma ferramenta gráfica simples e resiliente integrada ao **Nemo File Manager** para gerenciar downloads instáveis (focada no Anna's Archive).

O **Lazarus** foi projetado para ressuscitar downloads falhos. Se um download cai na metade, ele detecta o arquivo parcial, verifica o tamanho remoto e continua exatamente de onde parou (Range Request), validando o hash SHA256 ao final.

## ✨ Funcionalidades

- **Integração com Nemo:** Clique com botão direito em qualquer pasta > "Baixar URL aqui".
- **Captura de Clipboard:** Pega automaticamente a URL copiada.
- **Resume Inteligente:** Detecta arquivos parciais e tenta continuar o download (HTTP 206).
- **Troca de URL "Hot-Swap":** Se o link de download expirou (comum no Anna's Archive), você pode gerar um novo link, copiar, e clicar em "Nova URL" para continuar o download do **mesmo arquivo** usando o novo link.
- **Validação:** Cálculo automático de SHA256 ao final.

## 🚀 Instalação

### Pré-requisitos
- Linux com **Nemo** File Manager (padrão no Linux Mint).
- Python 3.

### Passo a passo

1. Clone o repositório:
   ```bash
   git clone https://github.com/dimasgomez/lazarus.git
   cd lazarus
