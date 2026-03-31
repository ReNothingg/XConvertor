import os
from PIL import Image
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
import pytesseract
from PyPDF2 import PdfReader
from docx2pdf import convert as docx_to_pdf_convert
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit
from .pdf_tools import PDFTools
from .file_utils import get_file_type

class ConversionError(Exception):
    pass

class Converter:
    def __init__(self):
        self.pdf_tools = PDFTools()

    def convert(self, input_paths, output_path, output_format, options=None):
        first_input = input_paths[0]
        file_type = get_file_type(first_input)
        
        try:
            if output_format == 'PDF (из изображений)':
                return self.pdf_tools.images_to_pdf(input_paths, output_path)
            if output_format == 'Объединить PDF':
                return self.pdf_tools.merge_pdfs(input_paths, output_path)
            if output_format == 'Разделить PDF':
                return self.pdf_tools.split_pdf(first_input, output_path)
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
            if file_type == 'document':
                return self.convert_from_docx(first_input, output_path, output_format)
            if file_type == 'text':
                return self.convert_from_text(first_input, output_path, output_format)
                    
            raise ConversionError("Неподдерживаемая комбинация конвертации.")
        except ConversionError:
            raise
        except Exception as e:
            raise ConversionError(f"Ошибка: {e}") from e

    def convert_image(self, input_path, output_path):
        with Image.open(input_path) as img:
            if output_path.lower().endswith(('.jpg', '.jpeg')) and img.mode in ('RGBA', 'P'):
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
            final_clip = clip_resized.subclip(0, min(duration, clip.duration))
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
                    text += (page.extract_text() or '') + '\n'
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            return output_path
        if out_format in ['JPG', 'PNG']:
            return self.pdf_tools.to_images(input_path, output_path, out_format.lower())
        raise ConversionError(f"Неподдерживаемый формат документа: {out_format}")

    def ocr_image(self, input_path, output_path):
        try:
            text = pytesseract.image_to_string(Image.open(input_path), lang='rus+eng')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            return output_path
        except pytesseract.TesseractNotFoundError:
            raise ConversionError("Tesseract не найден. Установите его и добавьте в PATH.")
        
    def convert_from_docx(self, input_path, output_path, out_format):
        if out_format == 'PDF':
            try:
                docx_to_pdf_convert(input_path, output_path)
                return output_path
            except Exception:
                raise ConversionError("Ошибка конвертации DOCX в PDF.\nУбедитесь, что у вас установлен MS Word или LibreOffice.")
        if out_format == 'TXT':
            document = Document(input_path)
            text = '\n'.join(paragraph.text for paragraph in document.paragraphs)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            return output_path

        raise ConversionError(f"Неподдерживаемый формат для DOCX: {out_format}")

    def convert_from_text(self, input_path, output_path, out_format):
        if out_format != 'PDF':
            raise ConversionError(f"Неподдерживаемый формат для TXT: {out_format}")

        with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()

        pdf = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        text_object = pdf.beginText(40, height - 40)

        for raw_line in lines:
            wrapped_lines = simpleSplit(raw_line.rstrip('\n'), 'Helvetica', 11, width - 80) or ['']
            for line in wrapped_lines:
                if text_object.getY() <= 40:
                    pdf.drawText(text_object)
                    pdf.showPage()
                    text_object = pdf.beginText(40, height - 40)
                text_object.textLine(line)

        pdf.drawText(text_object)
        pdf.save()
        return output_path
