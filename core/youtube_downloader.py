import yt_dlp
from PyQt5.QtCore import QObject, pyqtSignal

class YouTubeDownloader:
    def get_info(self, url):
        ydl_opts = {'noplaylist': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info

class DownloadWorker(QObject):
    finished = pyqtSignal(str)
    progress = pyqtSignal(int)
    error = pyqtSignal(str)

    def __init__(self, url, format_id, path):
        super().__init__()
        self.url = url
        self.format_id = format_id
        self.path = path

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            if total_bytes:
                downloaded_bytes = d.get('downloaded_bytes')
                percentage = (downloaded_bytes / total_bytes) * 100
                self.progress.emit(int(percentage))
        elif d['status'] == 'finished':
            self.progress.emit(100)

    def run(self):
        try:
            ydl_opts = {
                'format': self.format_id,
                'outtmpl': self.path,
                'progress_hooks': [self._progress_hook],
                'noplaylist': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            
            self.finished.emit(self.path)
        except Exception as e:
            self.error.emit(str(e))