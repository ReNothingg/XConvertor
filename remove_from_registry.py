# Запустите этот скрипт от имени администратора, чтобы удалить пункт в контекстное меню Windows Explorer.
# Он удаляет пункт "Конвертировать с XConvertor" для всех типов файлов

import winreg as reg

def remove_from_registry():
    try:
        key_path = r'*\\shell\\XConvertor'
        # Рекурсивно удаляем ключ command
        reg.DeleteKey(reg.HKEY_CLASSES_ROOT, f'{key_path}\\command')
        # Удаляем основной ключ
        reg.DeleteKey(reg.HKEY_CLASSES_ROOT, key_path)
        print("Успешно удалено из контекстного меню.")
    except FileNotFoundError:
        print("Запись в реестре не найдена. Возможно, она уже была удалена.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        print("Пожалуйста, убедитесь, что вы запускаете этот скрипт от имени администратора.")

if __name__ == "__main__":
    remove_from_registry()