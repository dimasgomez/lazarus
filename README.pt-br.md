# Lazarus Downloader for Anna's Archive (pt-br)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Linux](https://img.shields.io/badge/Linux-Mint%20%7C%20Nemo-green.svg)

Uma ferramenta de download resiliente com interface gráfica, integrada ao **Nemo File Manager** e projetada especificamente para downloads instáveis (como os do [Anna's Archive](https://annas-archive.li/)).

O **Lazarus** foi construído para "ressuscitar" downloads falhos. Se um download cair na metade, ele detecta o arquivo parcial, verifica o tamanho remoto e continua exatamente de onde parou (usando HTTP Range Requests), validando o hash SHA256 ao final. Tudo o que você precisa fazer é clicar com o botão direito (opcional) na mesma pasta e mandar baixar de novo. E de novo. Até a vitória.

Ele também funciona direto do terminal, basta ter copiado o link do Download antes de executar:

```bash
   nemo_downloader_ui_ressurector.py [destino]
```

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
