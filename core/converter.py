from PIL import Image
import os

class ConversionError(Exception):
    pass

class Converter:
    def convert(self, input_path, output_path, file_type, options=None):
        if file_type == 'image':
            return self.convert_image(input_path, output_path, options)                     
        else:
            raise ConversionError(f"Конвертация для типа '{file_type}' еще не поддерживается.")

    def convert_image(self, input_path, output_path, options=None):
        if options is None:
            options = {}
            
        try:
            
            img = Image.open(input_path)                                                
            if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
                if img.mode == 'RGBA' or img.mode == 'P':
                    img = img.convert('RGB')
           
            save_options = {}
            if 'quality' in options:
                save_options['quality'] = options['quality']                      
            img.save(output_path, **save_options)
            
            return output_path
            
        except Exception as e:
            
            raise ConversionError(f"Ошибка при конвертации изображения: {e}")

    
    def convert_audio(self, input_path, output_path, options=None):
        raise NotImplementedError("Функция конвертации аудио будет реализована.")

    def convert_video(self, input_path, output_path, options=None):
        raise NotImplementedError("Функция конвертации видео будет реализована.")

    def convert_document(self, input_path, output_path, options=None):
        raise NotImplementedError("Функция конвертации документов будет реализована.")