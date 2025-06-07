import os
import sys
import re
from PyQt5.QtCore import QLibraryInfo, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
                             QLineEdit, QComboBox, QFileDialog, QTextEdit, QMessageBox, QCheckBox)
import yt_dlp

# Fix for missing xcb plugin in PyInstaller-built app
if getattr(sys, 'frozen', False):
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(sys._MEIPASS, 'platforms')
else:
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = QLibraryInfo.location(QLibraryInfo.PluginsPath)


class ConsoleOutput(QObject):
    message = pyqtSignal(str)

    def write(self, msg):
        self.message.emit(str(msg))

    def flush(self):
        pass


class DownloadWorker(QThread):
    progress = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, download_type, links, resolution, download_path):
        super().__init__()
        self.download_type = download_type
        self.links = links
        self.resolution = resolution
        self.download_path = download_path

    def hook(self, d):
        if d['status'] == 'downloading':
            self.progress.emit(f"Downloading... {d['_percent_str']} completed.")
        elif d['status'] == 'finished':
            self.progress.emit(f"Finished downloading: {d['filename']}")

    def run(self):
        for link in self.links:
            try:
                if self.download_type == "Video":
                    self.download_video(link, self.resolution, self.download_path)
                elif self.download_type == "Audio":
                    self.download_mp3(link, self.download_path)
            except Exception as e:
                self.error.emit(f'Unexpected error: {e}')

    def download_video(self, video_url, resolution, download_path):
        try:
            ydl_opts = {
                'format': f'bestvideo[height<={resolution}]+bestaudio/best',
                'outtmpl': os.path.join(download_path, '%(title).100s.%(ext)s'),
                'merge_output_format': 'mp4',
                'progress_hooks': [self.hook],
                'verbose': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            self.progress.emit(f'Video downloaded: {video_url}')
        except Exception as e:
            self.error.emit(f'Error downloading video from {video_url}: {e}')

    def download_mp3(self, video_url, download_path):
        try:
            ydl_opts = {
                'format': 'bestaudio[ext=m4a]',
                'outtmpl': os.path.join(download_path, '%(title).100s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
                'progress_hooks': [self.hook],
                'verbose': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            self.progress.emit(f'Audio downloaded: {video_url}')
        except Exception as e:
            self.error.emit(f'Error downloading audio from {video_url}: {e}')


class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('YouTube Downloader')
        self.setGeometry(100, 100, 600, 700)
        self.setStyleSheet("""
            QWidget { background-color: #2e2e2e; color: #ffffff; font-family: Arial; }
            QLabel { font-size: 14px; }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #444; color: #fff; border: 1px solid #555;
                padding: 5px; border-radius: 3px;
            }
            QPushButton {
                background-color: #007bff; color: #fff; border: none;
                padding: 10px; border-radius: 5px; font-size: 16px;
            }
            QPushButton:hover { background-color: #0056b3; }
            QPushButton:pressed { background-color: #004494; }
            QComboBox QAbstractItemView {
                background-color: #444; color: #fff; border: 1px solid #555;
            }
        """)

        layout = QVBoxLayout()

        self.type_label = QLabel("Choose the type of download:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Video", "Audio"])
        layout.addWidget(self.type_label)
        layout.addWidget(self.type_combo)

        self.res_label = QLabel("Choose the resolution:")
        self.res_combo = QComboBox()
        self.res_combo.addItems(["720", "1080", "2160"])
        layout.addWidget(self.res_label)
        layout.addWidget(self.res_combo)

        self.link_label = QLabel("Enter YouTube links (one per line):")
        self.link_input = QTextEdit()
        layout.addWidget(self.link_label)
        layout.addWidget(self.link_input)

        self.folder_label = QLabel("Choose download folder:")
        self.folder_input = QLineEdit()
        self.folder_button = QPushButton("Browse")
        self.folder_button.clicked.connect(self.browse_folder)
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_input)
        layout.addWidget(self.folder_button)

        # --- Added Open Folder button here ---
        self.open_folder_button = QPushButton("Open Folder")
        self.open_folder_button.clicked.connect(self.open_folder)
        layout.addWidget(self.open_folder_button)

        self.default_folder_checkbox = QCheckBox("Set this as default download folder")
        layout.addWidget(self.default_folder_checkbox)

        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        layout.addWidget(self.console_output)

        self.download_button = QPushButton("Start Download")
        self.download_button.clicked.connect(self.start_download)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

        self.console = ConsoleOutput()
        self.console.message.connect(self.console_output.append)
        sys.stdout = self.console

        self.type_combo.currentIndexChanged.connect(self.toggle_resolution)

        self.show()
        self.load_default_folder()

    def closeEvent(self, event):
        sys.stdout = sys.__stdout__
        super().closeEvent(event)

    def toggle_resolution(self):
        is_video = self.type_combo.currentText() == "Video"
        self.res_label.setVisible(is_video)
        self.res_combo.setVisible(is_video)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if folder:
            self.folder_input.setText(folder)

    def open_folder(self):
        folder_path = self.folder_input.text()
        if os.path.isdir(folder_path):
            # Linux
            if sys.platform.startswith('linux'):
                os.system(f'xdg-open "{folder_path}"')
            # macOS
            elif sys.platform == 'darwin':
                os.system(f'open "{folder_path}"')
            # Windows
            elif sys.platform.startswith('win'):
                os.startfile(folder_path)
        else:
            QMessageBox.warning(self, "Folder Not Found", "The specified folder does not exist.")

    def load_default_folder(self):
        default_folder = self.get_default_folder()
        if default_folder:
            self.folder_input.setText(default_folder)

    def get_default_folder(self):
        if os.path.exists('default_folder.txt'):
            with open('default_folder.txt', 'r') as file:
                return file.read().strip()
        return None

    def set_default_folder(self, folder):
        with open('default_folder.txt', 'w') as file:
            file.write(folder)

    def is_valid_youtube_link(self, link):
        pattern = re.compile(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.be)\/.+$')
        return bool(pattern.match(link.strip()))

    def start_download(self):
        download_type = self.type_combo.currentText()
        links = [l.strip() for l in self.link_input.toPlainText().strip().split('\n') if l.strip()]
        download_path = self.folder_input.text()

        if not links or not download_path:
            QMessageBox.warning(self, "Input Error", "Please provide valid links and a download folder.")
            return

        if not all(self.is_valid_youtube_link(link) for link in links):
            QMessageBox.warning(self, "Invalid Link", "One or more links are not valid YouTube URLs.")
            return

        if self.default_folder_checkbox.isChecked():
            self.set_default_folder(download_path)

        resolution = self.res_combo.currentText() if download_type == "Video" else None
        download_path = os.path.join(download_path, download_type.lower())
        os.makedirs(download_path, exist_ok=True)

        self.download_button.setEnabled(False)
        self.worker = DownloadWorker(download_type, links, resolution, download_path)
        self.worker.progress.connect(self.console_output.append)
        self.worker.error.connect(lambda e: QMessageBox.critical(self, "Download Error", e))
        self.worker.finished.connect(lambda: self.download_button.setEnabled(True))
        self.worker.start()


def main():
    app = QApplication(sys.argv)
    downloader = YouTubeDownloader()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
