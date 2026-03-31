import os

IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff']
AUDIO_EXTENSIONS = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a']
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mkv', '.mov', '.webm', '.wmv']
DOCUMENT_EXTENSIONS = ['.docx']
TEXT_EXTENSIONS = ['.txt']

SPECIAL_ACTIONS = {
    'image': ['PDF (из изображений)', 'OCR (распознать текст)'],
    'pdf': ['DOCX', 'TXT', 'JPG', 'PNG', 'Объединить PDF', 'Разделить PDF']
}


def _dedupe_keep_order(items):
    seen = set()
    unique_items = []

    for item in items:
        if item not in seen:
            seen.add(item)
            unique_items.append(item)

    return unique_items


def get_file_type(filepath):
    extension = os.path.splitext(filepath)[1].lower()
    if extension in IMAGE_EXTENSIONS:
        return 'image'
    if extension in AUDIO_EXTENSIONS:
        return 'audio'
    if extension in VIDEO_EXTENSIONS:
        return 'video'
    if extension == '.pdf':
        return 'pdf'
    if extension in DOCUMENT_EXTENSIONS:
        return 'document'
    if extension in TEXT_EXTENSIONS:
        return 'text'
    return 'unknown'


def get_output_formats(file_type, filepath=None):
    formats = []
    extension = os.path.splitext(filepath)[1].lower() if filepath else ''

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
    elif file_type == 'document' and extension == '.docx':
        formats.append('PDF')
        formats.append('TXT')
    elif file_type == 'text' and extension == '.txt':
        formats.append('PDF')

    return _dedupe_keep_order(formats)
