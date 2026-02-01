# Lazarus Downloader for Anna's Archive

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Linux](https://img.shields.io/badge/Linux-Mint%20%7C%20Nemo-green.svg)

A resilient, GUI-based download tool integrated into **Nemo File Manager**, designed specifically for unstable downloads (like those from [Anna's Archive](https://annas-archive.li/)).

**Lazarus** is built to "resurrect" failed downloads. If a download drops halfway, it detects the partial file, checks the remote size, and resumes exactly where it left off (using HTTP Range Requests), verifying the SHA256 hash upon completion. All you have to do is right-click in the same folder and try to download it again. And again. until victory.

It also works straight of the terminal, you only need to copy the link first.

   ```bash
      nemo_downloader_ui_ressurector.py [path_to_save_file]
   ```

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
   git clone https://github.com/dimasgomez/lazarus.git
   cd lazarus
