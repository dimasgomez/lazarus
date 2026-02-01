# Lazarus Downloader for Anna's Archive

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Linux](https://img.shields.io/badge/Linux-Mint%20%7C%20Nemo-green.svg)

A resilient, GUI-based download tool integrated into **Nemo File Manager**, designed specifically for unstable downloads (like those from Anna's Archive).

**Lazarus** is built to "resurrect" failed downloads. If a download drops halfway, it detects the partial file, checks the remote size, and resumes exactly where it left off (using HTTP Range Requests), verifying the SHA256 hash upon completion.

## ✨ Features

- **Nemo Integration:** Right-click inside any folder > "Download URL here (Lazarus)".
- **Clipboard Capture:** Automatically grabs the URL from your clipboard.
- **Smart Resume:** Detects partial files and attempts to continue the download (HTTP 206).
- **"Hot-Swap" URLs:** If a download link expires (common with Anna's Archive/slow mirrors), you can generate a *new* link, copy it, and click "New URL" to continue downloading the **same file** using the fresh link.
- **Validation:** Automatic SHA256 calculation.

## 🚀 Installation

### Prerequisites
- Linux with **Nemo** File Manager (default on Linux Mint).
- Python 3.

### Setup

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/lazarus-downloader.git](https://github.com/YOUR_USERNAME/lazarus-downloader.git)
   cd lazarus-downloader

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
   git clone [https://github.com/SEU_USUARIO/lazarus-downloader.git](https://github.com/SEU_USUARIO/lazarus-downloader.git)
   cd lazarus-downloader
