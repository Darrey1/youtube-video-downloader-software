import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QRadioButton, QVBoxLayout, QHBoxLayout, QProgressBar
from pytube import YouTube
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class DownloaderThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, url, download_path, is_video):
        super().__init__()
        self.url = url
        self.download_path = download_path
        self.is_video = is_video
        

    def run(self):
        yt = YouTube(self.url)
        if self.is_video:
           stream = yt.streams.get_highest_resolution()
           extension = stream.mime_type.split('/')[-1]
           name_of_file = f'{yt.title}.{extension}'
        else:
            stream = yt.streams.filter(only_audio=True).first()
            extension = 'mp3'
            name_of_file = f'{yt.title}.{extension}'
            #markFilename='*'
        total_bytes = stream.filesize
        bytes_downloaded = 0
        

        stream.download(self.download_path, filename=name_of_file)
        #on_progress_callback=lambda chunk, file_handle, bytes_remaining: self.update_progress(total_bytes - bytes_remaining, total_bytes))# if self.is_video else name_of_file)

        self.finished.emit()
    def update_progress(self, chunk, file_handle, bytes_remaining):
        total_bytes = file_handle.size
        bytes_downloaded = total_bytes - bytes_remaining
        progress_percent = (bytes_downloaded / total_bytes) * 100
        self.progress.emit(progress_percent)

class YouTubeDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.init_ui()

    def init_ui(self):
        self.url_label = QLabel("Enter YouTube URL:")
        self.url_input = QLineEdit()
        self.video_radio = QRadioButton("Download video")
        self.audio_radio = QRadioButton("Download audio")
        self.download_path_label = QLabel("Select download path:")
        self.download_path_input = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.download_button = QPushButton("Download")
        self.progress_bar = QProgressBar()

        self.video_radio.setChecked(True)

        self.browse_button.clicked.connect(self.browse_download_path)
        self.download_button.clicked.connect(self.start_download)

        layout = QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)

        layout.addWidget(self.video_radio)
        layout.addWidget(self.audio_radio)

        layout.addWidget(self.download_path_label)
        layout.addWidget(self.download_path_input)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.download_button)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def browse_download_path(self):
        download_path = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if download_path:
            self.download_path_input.setText(download_path)

    def start_download(self):
        url = self.url_input.text()
        download_path = self.download_path_input.text()

        if not url or not download_path:
            return

        is_video = self.video_radio.isChecked()
        self.progress_bar.setValue(0)

        self.downloader_thread = DownloaderThread(url, download_path, is_video)
        self.downloader_thread.progress.connect(self.update_progress)
        self.downloader_thread.finished.connect(self.download_finished)

        self.downloader_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def download_finished(self):
        self.progress_bar.setValue(100)
        self.progress_bar.reset()
        self.url_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YouTubeDownloaderApp()
    window.show()
    sys.exit(app.exec())
