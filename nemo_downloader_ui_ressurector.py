#!/usr/bin/env python3
import sys
import os
import time
import hashlib
import urllib.request
import urllib.parse
import urllib.error
import subprocess
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
    QTextEdit,
    QWidget,
)
from PySide6.QtCore import Qt, QThread, Signal, Slot, QTimer


# --- WORKER THREAD ---
class DownloadWorker(QThread):
    progress_signal = Signal(int, str, str)
    log_signal = Signal(str)
    finished_signal = Signal(bool, str, str)  # sucesso, path_completo, hash

    def __init__(self, url, target_dir, force_existing_path=None):
        super().__init__()
        self.url = url
        self.target_dir = target_dir
        self.force_existing_path = (
            force_existing_path  # Se definido, força uso deste arquivo
        )
        self.is_running = True

    def get_filename_from_headers(self, response):
        try:
            content_disposition = response.headers.get("Content-Disposition")
            if content_disposition:
                parts = content_disposition.split("filename=")
                if len(parts) > 1:
                    name = parts[1].split(";")[0].strip("\"'")
                    return urllib.parse.unquote(name)
        except:
            pass
        path = urllib.parse.urlparse(self.url).path
        filename = os.path.basename(path)
        if not filename:
            filename = "download_unnamed.dat"
        return urllib.parse.unquote(filename)

    def calculate_sha256(self, filepath):
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(65536), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            return f"Erro: {e}"

    def run(self):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
            }

            # --- FASE 1: DEFINIÇÃO DO ARQUIVO ALVO ---
            self.log_signal.emit(f"Conectando...")
            self.progress_signal.emit(0, "-- KB/s", "Negociando...")

            req_probe = urllib.request.Request(self.url, headers=headers)

            resume_byte_pos = 0
            file_mode = "wb"
            save_path = ""
            total_size_remote = 0

            # Se já temos um arquivo forçado (Troca de URL), usamos ele
            if self.force_existing_path and os.path.exists(self.force_existing_path):
                save_path = self.force_existing_path
                self.log_signal.emit(
                    f"♻️ REUTILIZANDO ARQUIVO PARCIAL:\n{os.path.basename(save_path)}"
                )

                # Sonda apenas para pegar tamanho remoto (se possível)
                try:
                    with urllib.request.urlopen(req_probe, timeout=15) as probe:
                        cl = probe.headers.get("content-length")
                        if cl:
                            total_size_remote = int(cl)
                except:
                    self.log_signal.emit(
                        "Aviso: Não foi possível sondar tamanho remoto. Tentando resume cego."
                    )

            else:
                # Fluxo normal: descobre nome via Headers
                with urllib.request.urlopen(req_probe, timeout=30) as response_probe:
                    filename = self.get_filename_from_headers(response_probe)
                    save_path = os.path.join(self.target_dir, filename)
                    cl = response_probe.headers.get("content-length")
                    if cl:
                        total_size_remote = int(cl)

            # --- FASE 2: VERIFICAÇÃO DE RESUME ---
            if os.path.exists(save_path):
                local_size = os.path.getsize(save_path)
                if local_size > 0:
                    self.log_signal.emit(
                        f"Local: {local_size / (1024 * 1024):.2f} MB | Remoto: {total_size_remote / (1024 * 1024):.2f} MB"
                    )

                    if total_size_remote > 0 and local_size < total_size_remote:
                        self.log_signal.emit(">> MODO RESUME ATIVADO <<")
                        resume_byte_pos = local_size
                        file_mode = "ab"
                        headers["Range"] = f"bytes={resume_byte_pos}-"
                    elif total_size_remote == 0:
                        self.log_signal.emit(
                            "Tamanho remoto desconhecido. Tentando resume (Append)..."
                        )
                        resume_byte_pos = local_size
                        file_mode = "ab"
                        headers["Range"] = f"bytes={resume_byte_pos}-"
                    else:
                        if self.force_existing_path:
                            self.log_signal.emit("⚠️ AVISO: Arquivo local >= Remoto.")
                            self.log_signal.emit(">> FORÇANDO RESUME (A PEDIDO) <<")
                            # Em vez de erro, forçamos o modo append
                            resume_byte_pos = local_size
                            file_mode = "ab"
                            headers["Range"] = f"bytes={resume_byte_pos}-"
                        else:
                            self.log_signal.emit(
                                "Arquivo local completo/maior. Sobrescrevendo."
                            )
                            resume_byte_pos = 0

            # --- FASE 3: DOWNLOAD REAL ---
            req_download = urllib.request.Request(self.url, headers=headers)

            with urllib.request.urlopen(req_download, timeout=60) as response:
                if response.getcode() == 206:
                    self.log_signal.emit(f"Servidor aceitou Resume (206)!")
                elif resume_byte_pos > 0:
                    self.log_signal.emit(
                        f"Servidor recusou Resume (Code {response.getcode()})."
                    )
                    if self.force_existing_path:
                        raise Exception(
                            "Servidor novo não aceita resume. Impossível continuar arquivo antigo."
                        )
                    self.log_signal.emit("Reiniciando do zero.")
                    resume_byte_pos = 0
                    file_mode = "wb"

                content_len = response.headers.get("content-length")
                remaining_size = int(content_len) if content_len else 0
                full_file_size = resume_byte_pos + remaining_size

                downloaded = resume_byte_pos
                block_size = 65536
                start_time = time.time()

                with open(save_path, file_mode) as f:
                    while self.is_running:
                        buffer = response.read(block_size)
                        if not buffer:
                            break
                        f.write(buffer)
                        downloaded += len(buffer)

                        if full_file_size > 0:
                            percent = int((downloaded / full_file_size) * 100)
                        else:
                            percent = 0

                        elapsed = time.time() - start_time
                        if elapsed > 0:
                            current_dl = downloaded - resume_byte_pos
                            speed = current_dl / elapsed
                            speed_str = (
                                f"{speed / 1024 / 1024:.2f} MB/s"
                                if speed > 1024 * 1024
                                else f"{speed / 1024:.2f} KB/s"
                            )
                        else:
                            speed_str = "-- KB/s"

                        self.progress_signal.emit(percent, speed_str, "Baixando...")

                if self.is_running:
                    self.progress_signal.emit(
                        100, "Finalizando", "Calculando Checksum..."
                    )
                    self.log_signal.emit("Verificando SHA256...")
                    file_hash = self.calculate_sha256(save_path)
                    self.log_signal.emit(f"HASH: {file_hash}")
                    self.finished_signal.emit(True, save_path, file_hash)
                else:
                    self.log_signal.emit("Interrompido pelo usuário.")
                    self.finished_signal.emit(False, "Cancelado.", "")

        except Exception as e:
            self.log_signal.emit(f"ERRO: {str(e)}")
            self.finished_signal.emit(False, str(e), "")

    def stop(self):
        self.is_running = False


# --- GUI ---
class DownloadDialog(QDialog):
    def __init__(self, target_dir):
        super().__init__()
        self.target_dir = target_dir
        self.url = self.get_clipboard_url()
        self.worker = None
        self.can_close = True
        self.saved_file_path = None  # Caminho do arquivo sendo baixado (para resume)

        self.init_ui()

        if self.url:
            QTimer.singleShot(500, self.start_download)
        else:
            self.log("ERRO: Nenhuma URL na área de transferência.")
            self.btn_close.setText("Fechar")
            self.btn_close.setEnabled(True)
            self.lbl_status.setText("SEM URL")
            self.lbl_status.setStyleSheet(
                "color: orange; font-weight: bold; font-size: 22px;"
            )

    def init_ui(self):
        self.setWindowTitle("Lazarus Downloader for Anna's Archive")
        self.setMinimumWidth(650)
        self.setMinimumHeight(500)
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowStaysOnTopHint
            | Qt.WindowCloseButtonHint
            | Qt.WindowMinimizeButtonHint
        )

        layout = QVBoxLayout(self)

        # Status
        self.lbl_status = QLabel("Aguardando...")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.lbl_status.setStyleSheet(
            "font-weight: bold; font-size: 18px; color: #888;"
        )
        layout.addWidget(self.lbl_status)

        # URL
        url_display = self.url if self.url else "---"
        self.lbl_url = QLabel(f"{url_display}")
        self.lbl_url.setStyleSheet("color: gray; font-size: 10px;")
        self.lbl_url.setWordWrap(True)
        layout.addWidget(self.lbl_url)

        # Barra
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setStyleSheet(
            "QProgressBar { height: 30px; text-align: center; font-weight: bold; }"
        )
        layout.addWidget(self.progress_bar)

        # Velocidade
        self.lbl_details = QLabel("-- KB/s")
        self.lbl_details.setAlignment(Qt.AlignRight)
        self.lbl_details.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.lbl_details)

        # Log
        self.log_viewer = QTextEdit()
        self.log_viewer.setReadOnly(True)
        self.log_viewer.setStyleSheet("""
            background-color: #1e1e1e;
            color: #00ff00;
            font-family: monospace;
            font-size: 11px;
            border: 1px solid #444;
        """)
        layout.addWidget(self.log_viewer)

        # --- BOTÕES ---
        self.action_layout = QHBoxLayout()

        # Botões de Sucesso
        self.btn_open_file = QPushButton("📄 Abrir Arquivo")
        self.btn_open_file.clicked.connect(self.open_file)
        self.btn_open_file.hide()

        self.btn_open_folder = QPushButton("📂 Abrir Local")
        self.btn_open_folder.clicked.connect(self.open_folder)
        self.btn_open_folder.hide()

        # Botões de Fracasso
        self.btn_retry = QPushButton("↻ Tentar Novamente")
        self.btn_retry.setStyleSheet(
            "background-color: #ffaa00; color: black; font-weight: bold;"
        )
        self.btn_retry.clicked.connect(self.retry_download)
        self.btn_retry.hide()

        self.btn_new_url = QPushButton("🔗 Nova URL (Manter arquivo)")
        self.btn_new_url.setToolTip(
            "Use isso se o link expirou mas você quer continuar o mesmo arquivo."
        )
        self.btn_new_url.setStyleSheet(
            "background-color: #00aaff; color: white; font-weight: bold;"
        )
        self.btn_new_url.clicked.connect(self.change_url_and_resume)
        self.btn_new_url.hide()

        self.action_layout.addWidget(self.btn_open_file)
        self.action_layout.addWidget(self.btn_open_folder)
        self.action_layout.addWidget(self.btn_retry)
        self.action_layout.addWidget(self.btn_new_url)
        self.action_layout.addStretch()

        self.btn_close = QPushButton("Inicializando...")
        self.btn_close.setEnabled(False)
        self.btn_close.setMinimumWidth(120)
        self.btn_close.clicked.connect(self.accept)
        self.action_layout.addWidget(self.btn_close)

        layout.addLayout(self.action_layout)

    def get_clipboard_url(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text().strip()
        if text.startswith(("http://", "https://", "ftp://")):
            return text
        return None

    def log(self, msg):
        self.log_viewer.append(f"[{time.strftime('%H:%M:%S')}] {msg}")
        self.log_viewer.verticalScrollBar().setValue(
            self.log_viewer.verticalScrollBar().maximum()
        )

    def start_download(self, force_existing_path=None):
        if not self.url:
            return

        # Reset UI
        self.can_close = False
        self.btn_close.setText("Baixando...")
        self.btn_close.setEnabled(False)
        self.btn_retry.hide()
        self.btn_new_url.hide()
        self.lbl_status.setText("CONECTANDO...")
        self.lbl_status.setStyleSheet(
            "color: #4488ff; font-weight: bold; font-size: 18px;"
        )

        self.log("-" * 40)
        self.log(f"Iniciando: {self.url[:50]}...")
        if force_existing_path:
            self.log(f"Forçando arquivo alvo: {force_existing_path}")
            self.saved_file_path = (
                force_existing_path  # Garante que sabemos qual é o arquivo
            )

        self.worker = DownloadWorker(self.url, self.target_dir, force_existing_path)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.log_signal.connect(self.log)
        self.worker.finished_signal.connect(self.download_finished)
        self.worker.start()

    @Slot(int, str, str)
    def update_progress(self, percent, speed, status):
        self.progress_bar.setValue(percent)
        self.lbl_details.setText(speed)
        # Se estivermos baixando, só atualiza o texto se não for o status final
        if self.worker.is_running:
            self.lbl_status.setText(status)

    @Slot(bool, str, str)
    def download_finished(self, success, full_path, file_hash):
        self.can_close = True
        self.btn_close.setEnabled(True)

        # Guarda o caminho caso tenhamos falhado, para poder resumir depois
        if full_path and os.path.exists(full_path):
            self.saved_file_path = full_path

        if success:
            self.progress_bar.setValue(100)
            self.lbl_status.setText("SUCESSO!")
            self.lbl_status.setStyleSheet(
                "color: #00FF00; font-weight: bold; font-size: 24px;"
            )  # GARRAFAL

            self.log("-" * 40)
            self.log("DOWNLOAD FINALIZADO")
            self.log(f"Local: {full_path}")
            self.log("-" * 40)

            self.btn_close.setText("Fechar")
            self.btn_open_file.show()
            self.btn_open_folder.show()
            self.btn_retry.setText("Forçar Resume")  # Opcional: mudar o texto
            self.btn_retry.show()
            QApplication.beep()
        else:
            self.lbl_status.setText("FALHA")
            self.lbl_status.setStyleSheet(
                "color: #FF0000; font-weight: bold; font-size: 24px;"
            )  # GARRAFAL
            self.progress_bar.setStyleSheet(
                "QProgressBar::chunk { background-color: #ff4444; }"
            )

            self.log("-" * 40)
            self.log(f"ERRO: {full_path}")
            if self.saved_file_path:
                self.log(f"Arquivo parcial salvo em: {self.saved_file_path}")
            self.log("-" * 40)

            self.btn_close.setText("Fechar")
            self.btn_retry.show()
            # Só mostra Nova URL se tivermos um arquivo parcial para salvar
            if self.saved_file_path:
                self.btn_new_url.show()
            QApplication.beep()

    def retry_download(self):
        self.progress_bar.setStyleSheet(
            "QProgressBar::chunk { background-color: #00ccff; }"
        )  # Reseta cor
        self.start_download(force_existing_path=self.saved_file_path)

    def change_url_and_resume(self):
        new_url = self.get_clipboard_url()
        if not new_url:
            QMessageBox.warning(
                self, "Erro", "Copie a NOVA URL para a área de transferência primeiro!"
            )
            return

        if new_url == self.url:
            reply = QMessageBox.question(
                self,
                "Mesma URL",
                "A URL na área de transferência é IGUAL à anterior.\nDeseja usar assim mesmo?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply == QMessageBox.No:
                return

        self.log(f"🔄 Trocando URL de origem...")
        self.log(f"Antiga: {self.url[:30]}...")
        self.log(f"Nova:   {new_url[:30]}...")

        self.url = new_url
        self.lbl_url.setText(f"{self.url}")

        # Reinicia forçando o arquivo antigo
        self.progress_bar.setStyleSheet(
            "QProgressBar::chunk { background-color: #00ccff; }"
        )
        self.start_download(force_existing_path=self.saved_file_path)

    def open_file(self):
        if self.saved_file_path and os.path.exists(self.saved_file_path):
            try:
                subprocess.Popen(["xdg-open", self.saved_file_path])
            except:
                pass

    def open_folder(self):
        if self.saved_file_path:
            try:
                subprocess.Popen(["nemo", self.saved_file_path])
            except:
                pass

    def closeEvent(self, event):
        if not self.can_close:
            reply = QMessageBox.question(
                self,
                "Cancelar?",
                "Download em andamento. Cancelar?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                if self.worker:
                    self.worker.stop()
                    self.worker.wait(1000)
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    target_dir = sys.argv[1] if len(sys.argv) > 1 else str(Path.home())
    if not os.path.isdir(target_dir):
        sys.exit(1)
    dialog = DownloadDialog(target_dir)
    dialog.show()
    sys.exit(app.exec())
