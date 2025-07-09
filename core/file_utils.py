import os

IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff']
AUDIO_EXTENSIONS = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a']
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mkv', '.mov', '.webm', '.wmv']
DOCUMENT_EXTENSIONS = ['.pdf', '.docx', '.doc', '.txt', '.rtf', '.epub']

SPECIAL_ACTIONS = {
    'image': ['PDF (из изображений)', 'OCR (распознать текст)'],
    'pdf': ['DOCX', 'TXT', 'JPG', 'PNG', 'Объединить PDF', 'Разделить PDF']
}

def get_file_type(filepath):
    extension = os.path.splitext(filepath)[1].lower()
    if extension in IMAGE_EXTENSIONS: return 'image'
    if extension in AUDIO_EXTENSIONS: return 'audio'
    if extension in VIDEO_EXTENSIONS: return 'video'
    if extension in DOCUMENT_EXTENSIONS: return 'document'
    if extension == '.pdf': return 'pdf'
    return 'unknown'

def get_output_formats(file_type, filepath):
    formats = []
    extension = os.path.splitext(filepath)[1].lower()

    if file_type == 'image':
        formats.extend([ext.upper().replace('.', '') for ext in IMAGE_EXTENSIONS])
        formats.extend(SPECIAL_ACTIONS['image'])
    elif file_type == 'audio':
        formats.extend([ext.upper().replace('.', '') for ext in AUDIO_EXTENSIONS])
    elif file_type == 'video':
        video_formats = [ext.upper().replace('.', '') for ext in VIDEO_EXTENSIONS]
        audio_formats = [f"{ext.upper().replace('.', '')} (аудио)" for ext in AUDIO_EXTENSIONS]
        formats.extend(video_formats)
        formats.extend(audio_formats)
        formats.append('GIF (анимация)')
    elif file_type == 'pdf':
        formats.extend(SPECIAL_ACTIONS['pdf'])
    elif extension == '.docx':
        formats.append('PDF')
        formats.append('TXT')
    return sorted(list(set(formats)))
