import os

IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff']
AUDIO_EXTENSIONS = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a']
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mkv', '.mov', '.webm', '.wmv']
DOCUMENT_EXTENSIONS = ['.pdf', '.docx', '.doc', '.txt', '.rtf', '.epub']

def get_file_type(filepath):
    extension = os.path.splitext(filepath)[1].lower()
    
    if extension in IMAGE_EXTENSIONS:
        return 'image'
    if extension in AUDIO_EXTENSIONS:
        return 'audio'
    if extension in VIDEO_EXTENSIONS:
        return 'video'
    if extension in DOCUMENT_EXTENSIONS:
        return 'document'
        
    return 'unknown'

def get_output_formats(file_type):
    if file_type == 'image':
        return [ext.replace('.', '').upper() for ext in IMAGE_EXTENSIONS]
    
    elif file_type == 'audio':
        return [ext.replace('.', '').upper() for ext in AUDIO_EXTENSIONS]
        
    elif file_type == 'video':
        video_formats = [ext.replace('.', '').upper() for ext in VIDEO_EXTENSIONS]
        audio_formats_from_video = [f"{ext.replace('.', '').upper()} (только аудио)" for ext in AUDIO_EXTENSIONS]
        return video_formats + audio_formats_from_video
        
    elif file_type == 'document':
        return [ext.replace('.', '').upper() for ext in DOCUMENT_EXTENSIONS]
        
    return []