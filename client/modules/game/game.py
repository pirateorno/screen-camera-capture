import tkinter as tk
import pygame.mixer
import os
import random
import json

# Инициализация Pygame и звуков
pygame.mixer.init()

# Путь к файлу для сохранения состояния игры
SAVE_FILE_PATH = "game_state.json"

# Инициализация переменных по умолчанию
default_game_state = {
    "clicks": 0,
    "click_increment": 1,
    "upgrade_cost": 100
}

# Функция для загрузки состояния игры из файла
def load_game_state():
    if os.path.exists(SAVE_FILE_PATH):
        with open(SAVE_FILE_PATH, "r") as file:
            return json.load(file)
    else:
        return default_game_state

# Функция для сохранения состояния игры в файл
def save_game_state(game_state):
    with open(SAVE_FILE_PATH, "w") as file:
        json.dump(game_state, file)

# Функция для воспроизведения случайного звука
def play_random_sound():
    sound_files = os.listdir("sounds")
    sound_file = random.choice(sound_files)
    pygame.mixer.music.load(os.path.join("sounds", sound_file))
    pygame.mixer.music.play()

# Функция для обновления метки с количеством кликов
def update_clicks_label():
    clicks_label.config(text="Рабы: " + str(game_state["clicks"]))

# Функция для обработки клика
def click():
    game_state["clicks"] += game_state["click_increment"]
    update_clicks_label()
    play_random_sound()
    save_game_state(game_state)

# Функция для сброса прогресса
def reset_clicks():
    game_state["clicks"] = 0
    update_clicks_label()
    save_game_state(game_state)

# Функция для улучшения
def upgrade_clicks():
    if game_state["clicks"] >= game_state["upgrade_cost"]:
        game_state["clicks"] -= game_state["upgrade_cost"]
        game_state["click_increment"] += 1
        game_state["upgrade_cost"] *= 2
        upgrade_button.config(text=f"Прокачать - {game_state['upgrade_cost']}")
        update_clicks_label()
        save_game_state(game_state)

# Создание главного окна
root = tk.Tk()
root.title("нигер")

# Загрузка состояния игры
game_state = load_game_state()

# Создание виджетов
clicks_label = tk.Label(root, text="Рабы: " + str(game_state["clicks"]), font=("Helvetica", 24))
clicks_label.pack(pady=20)

click_button = tk.Button(root, text="Раб", font=("Helvetica", 18), command=click)
click_button.pack(pady=10)

reset_button = tk.Button(root, text="Продать", font=("Helvetica", 12), command=reset_clicks)
reset_button.pack(pady=5)

upgrade_button = tk.Button(root, text=f"Прокачать - {game_state['upgrade_cost']}", font=("Helvetica", 12), command=upgrade_clicks)
upgrade_button.pack(pady=5)

# Запуск главного цикла
root.mainloop()
