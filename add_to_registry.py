# Запустите этот скрипт от имени администратора, чтобы добавить пункт в контекстное меню Windows Explorer.
# Он добавляет пункт "Конвертировать с XConvertor" для всех типов файлов

import sys
import os
import winreg as reg

def add_to_registry():
    try:
        # Получаем абсолютные пути к интерпретатору Python и главному скрипту
        python_exe = sys.executable
        # Используем pythonw.exe для запуска без консольного окна
        pythonw_exe = python_exe.replace("python.exe", "pythonw.exe") 
        script_path = os.path.abspath("main.py")

        # Ключ реестра для всех типов файлов (*)
        key_path = r'*\\shell\\XConvertor'
        
        # Создаем ключ XConvertor
        key = reg.CreateKey(reg.HKEY_CLASSES_ROOT, key_path)
        # Устанавливаем текст, который будет отображаться в меню
        reg.SetValue(key, '', reg.REG_SZ, 'Конвертировать с XConvertor')
        # Добавляем иконку
        reg.SetValueEx(key, 'Icon', 0, reg.REG_SZ, os.path.abspath("assets/icons/logo.png"))
        reg.CloseKey(key)

        # Создаем вложенный ключ command
        key = reg.CreateKey(reg.HKEY_CLASSES_ROOT, f'{key_path}\\command')
        # Устанавливаем команду для выполнения. "%1" - это плейсхолдер для пути к файлу
        command = f'"{pythonw_exe}" "{script_path}" "%1"'
        reg.SetValue(key, '', reg.REG_SZ, command)
        reg.CloseKey(key)

        print("Успешно добавлено в контекстное меню!")
        print("Теперь можно кликнуть правой кнопкой по любому файлу и выбрать 'Конвертировать с XConvertor'.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        print("Пожалуйста, убедитесь, что вы запускаете этот скрипт от имени администратора.")

if __name__ == "__main__":
    add_to_registry()