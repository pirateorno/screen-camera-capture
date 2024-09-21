import tkinter as tk
from PIL import Image, ImageTk
import time
import pygame
import os
import random

def lift_window(window):
    window.attributes('-topmost', True)
    window.update_idletasks()  # get window on top
    #window.attributes('-topmost', False)  # prevent permanent focus
    window.focus_force()  # focus to the window

def show_screamer(duration):
    base_dir = os.path.dirname(__file__)

    images = ['screamer.jpg', 'best_screamer.jpeg']
    random_image = random.choice(images)

    sounds = ['screamer.mp3', 'best_screamer.mp3']
    random_sound = random.choice(sounds)


    image_path = os.path.join(base_dir, '..', 'misc', random_image)
    sound_path = os.path.join(base_dir, '..', 'misc', random_sound)
    # Инициализация pygame
    pygame.init()
    pygame.mixer.init()

    # Загрузка звука
    sound = pygame.mixer.Sound(sound_path)

    # Создаем главное окно
    root = tk.Tk()
    root.attributes('-fullscreen', True)  # Делает окно на весь экран

    # Поднимаем окно на передний план
    lift_window(root)

    # Получаем размеры экрана
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Загружаем изображение
    image = Image.open(image_path)

    # Растягиваем изображение до размеров экрана
    image = image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)

    # Создаем метку для изображения
    label = tk.Label(root, image=photo)
    label.pack(fill=tk.BOTH, expand=True)

    # Воспроизводим звук
    sound.play()

    # Обновляем окно и ждем
    root.update()
    time.sleep(duration)

    # Закрываем окно и останавливаем звук
    pygame.mixer.quit()
    root.destroy()