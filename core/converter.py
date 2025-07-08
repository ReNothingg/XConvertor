from PIL import Image
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
import os

from .file_utils import AUDIO_EXTENSIONS 

class ConversionError(Exception):
    pass

class Converter:
    def convert(self, input_path, output_path, file_type, options=None):
        output_extension = os.path.splitext(output_path)[1].lower()

        if file_type == 'image':
            return self.convert_image(input_path, output_path, options)
            
        elif file_type == 'audio':
            return self.convert_audio(input_path, output_path, options)
            
        elif file_type == 'video':
            if output_extension in AUDIO_EXTENSIONS:
                return self.extract_audio_from_video(input_path, output_path, options)
            else:
                return self.convert_video(input_path, output_path, options)
        else:
            raise ConversionError(f"Конвертация для типа '{file_type}' еще не поддерживается.")

    def convert_image(self, input_path, output_path, options=None):
        if options is None:
            options = {}
        try:
            img = Image.open(input_path)
            if output_path.lower().endswith(('.jpg', '.jpeg')):
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
            
            save_options = {}
            if 'quality' in options:
                save_options['quality'] = options['quality']
            
            img.save(output_path, **save_options)
            return output_path
        except Exception as e:
            raise ConversionError(f"Ошибка при конвертации изображения: {e}")

    def convert_audio(self, input_path, output_path, options=None):
        """
        Конвертирует аудиофайл с помощью pydub.
        """
        try:
            output_format = os.path.splitext(output_path)[1][1:].lower()
            audio = AudioSegment.from_file(input_path)
            audio.export(output_path, format=output_format)
            return output_path
        except Exception as e:
            raise ConversionError(f"Ошибка при конвертации аудио: {e}\n\nУбедитесь, что FFmpeg установлен и доступен в PATH.")

    def convert_video(self, input_path, output_path, options=None):
        """
        Конвертирует видеофайл с помощью moviepy.
        """
        try:
            with VideoFileClip(input_path) as video:
                video.write_videofile(output_path, codec='libx264', audio_codec='aac')
            return output_path
        except Exception as e:
            raise ConversionError(f"Ошибка при конвертации видео: {e}\n\nУбедитесь, что FFmpeg установлен и доступен в PATH.")

    def extract_audio_from_video(self, input_path, output_path, options=None):
        try:
            with VideoFileClip(input_path) as video:
                if video.audio is None:
                    raise ConversionError("В выбранном видеофайле отсутствует аудиодорожка.")
                video.audio.write_audiofile(output_path)
            return output_path
        except Exception as e:
            raise ConversionError(f"Ошибка при извлечении аудио: {e}\n\nУбедитесь, что FFmpeg установлен и доступен в PATH.")

    def convert_document(self, input_path, output_path, options=None):
        raise NotImplementedError("Функция конвертации документов будет реализована.")