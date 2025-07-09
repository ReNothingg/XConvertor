from pytube import YouTube
from PyQt5.QtCore import QObject, pyqtSignal

class YouTubeDownloader:
    def __init__(self):
        self.yt = None

    def get_streams(self, url):
        self.yt = YouTube(url)
        
        streams = self.yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        streams.extend(self.yt.streams.filter(adaptive=True, file_extension='mp4', type="video").order_by('resolution').desc())
        streams.extend(self.yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc())
        return streams

    def get_title(self, url):
        if not self.yt or self.yt.watch_url != url:
            self.yt = YouTube(url)
        return self.yt.title

    def get_default_filename(self, stream):
        return f"{self.yt.title}.{stream.subtype}"

class DownloadWorker(QObject):
    finished = pyqtSignal(str)
    progress = pyqtSignal(int)
    error = pyqtSignal(str)

    def __init__(self, stream, path):
        super().__init__()
        self.stream = stream
        self.path = path
        self.stream.yt.register_on_progress_callback(self.on_progress)

    def run(self):
        try:
            self.stream.download(output_path=self.path)
            self.finished.emit(self.path)
        except Exception as e:
            self.error.emit(str(e))

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        self.progress.emit(int(percentage))