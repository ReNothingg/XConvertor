from .youtube_downloader import YouTubeDownloader
import os
from PIL import Image
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
import pytesseract
from .pdf_tools import PDFTools

class ConversionError(Exception):
    pass

class Converter:
    def __init__(self):
        self.pdf_tools = PDFTools()
        self.youtube_downloader = YouTubeDownloader()

    def convert(self, input_paths, output_path, output_format, options=None):
        first_input = input_paths[0]
        
        try:
            if first_input.startswith(('http://youtube.com', 'https://youtube.com', 
                                     'http://www.youtube.com', 'https://www.youtube.com',
                                     'youtube.com', 'www.youtube.com')):
                if 'MP3' in output_format:
                    return self.youtube_downloader.download(first_input, output_path, 'mp3')
                else:
                    return self.youtube_downloader.download(first_input, output_path, 'mp4')
            file_type = self._get_file_type(first_input)
            
            if output_format == 'PDF (из изображений)':
                return self.pdf_tools.images_to_pdf(input_paths, output_path)
            if output_format == 'Объединить PDF':
                return self.pdf_tools.merge_pdfs(input_paths, output_path)
            if output_format == 'OCR (распознать текст)':
                return self.ocr_image(first_input, output_path)
            if file_type == 'pdf':
                return self.convert_document(first_input, output_path, output_format)
            if file_type == 'image':
                return self.convert_image(first_input, output_path)
            if file_type == 'audio':
                return self.convert_audio(first_input, output_path)
            if file_type == 'video':
                if 'аудио' in output_format:
                    return self.extract_audio_from_video(first_input, output_path)
                elif 'GIF' in output_format:
                    return self.convert_video_to_gif(first_input, output_path)
                else:
                    return self.convert_video(first_input, output_path)
                    
            raise ConversionError(f"Неподдерживаемая комбинация конвертации.")
        except Exception as e:
            raise ConversionError(f"Ошибка: {e}")

    def _get_file_type(self, path):
        ext = os.path.splitext(path)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff']: return 'image'
        if ext in ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a']: return 'audio'
        if ext in ['.mp4', '.avi', '.mkv', '.mov', '.webm', '.wmv']: return 'video'
        if ext == '.pdf': return 'pdf'
        return 'unknown'

    def convert_image(self, input_path, output_path):
        img = Image.open(input_path)
        if output_path.lower().endswith(('.jpg', '.jpeg')):
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
        img.save(output_path)
        return output_path

    def convert_audio(self, input_path, output_path):
        fmt = os.path.splitext(output_path)[1][1:]
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format=fmt)
        return output_path

    def convert_video(self, input_path, output_path):
        with VideoFileClip(input_path) as video:
            video.write_videofile(output_path, codec='libx264', audio_codec='aac')
        return output_path

    def extract_audio_from_video(self, input_path, output_path):
        with VideoFileClip(input_path) as video:
            if video.audio is None:
                raise ConversionError("В видео нет аудиодорожки.")
            video.audio.write_audiofile(output_path)
        return output_path
        
    def convert_video_to_gif(self, input_path, output_path, duration=5):
        with VideoFileClip(input_path) as clip:
            clip_resized = clip.resize(height=360)
            final_clip = clip_resized.subclip(0, duration)
            final_clip.write_gif(output_path, fps=15)
        return output_path

    def convert_document(self, input_path, output_path, out_format):
        if out_format == 'DOCX':
            return self.pdf_tools.to_docx(input_path, output_path)
        if out_format == 'TXT':
            text = ''
            with open(input_path, 'rb') as f:
                reader = PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + '\n'
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            return output_path
        if out_format in ['JPG', 'PNG']:
            return self.pdf_tools.to_images(input_path, os.path.dirname(output_path), out_format.lower())
        raise ConversionError(f"Неподдерживаемый формат документа: {out_format}")

    def ocr_image(self, input_path, output_path):
        try:
            text = pytesseract.image_to_string(Image.open(input_path), lang='rus+eng')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            return output_path
        except pytesseract.TesseractNotFoundError:
            raise ConversionError("Tesseract не найден. Установите его и добавьте в PATH.")