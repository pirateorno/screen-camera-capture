import psutil

# Имя процесса, который нужно закрыть
process_name = "opera.exe"

# Перебираем все запущенные процессы
for proc in psutil.process_iter(['pid', 'name']):
    try:
        # Проверяем имя процесса
        if proc.info['name'] == process_name:
            proc.terminate()  # Останавливаем процесс
            print(f"Процесс {process_name} (PID {proc.info['pid']}) завершен.")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
