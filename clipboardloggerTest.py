import pyperclip
import time

def monitor_clipboard():
    previous_clipboard_content = ''
    while True:
        clipboard_content = pyperclip.paste()
        if clipboard_content != previous_clipboard_content:
            print("Содержимое буфера обмена: ", clipboard_content)
            previous_clipboard_content = clipboard_content
        time.sleep(1)  # Добавляем паузу в 0.5 секунды

if __name__ == "__main__":
    monitor_clipboard()
