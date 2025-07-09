from pytube import YouTube
from moviepy.editor import VideoFileClip
import os

class YouTubeDownloader:
    def __init__(self):
        self.supported_formats = ['mp4', 'webm', 'mp3']

    def download(self, url, output_path, format='mp4'):
        try:
            yt = YouTube(url)
            
            if format in ['mp4', 'webm']:
                stream = yt.streams.filter(progressive=True, file_extension=format).order_by('resolution').desc().first()
                if not stream:
                    raise Exception(f"Не найден поток {format}")
                
                video_path = stream.download(output_path=os.path.dirname(output_path))
                os.rename(video_path, output_path)
                
            elif format == 'mp3':
                stream = yt.streams.filter(progressive=True).order_by('resolution').desc().first()
                temp_video = stream.download(output_path=os.path.dirname(output_path))
                
                with VideoFileClip(temp_video) as video:
                    video.audio.write_audiofile(output_path)
                
                os.remove(temp_video)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Ошибка при скачивании: {str(e)}")

    def get_video_info(self, url):
        try:
            yt = YouTube(url)
            return {
                'title': yt.title,
                'author': yt.author,
                'length': yt.length,
                'views': yt.views,
                'thumbnail_url': yt.thumbnail_url
            }
        except Exception as e:
            raise Exception(f"Ошибка при получении информации: {str(e)}")