import keyboard

# Список клавиш для игнорирования
keys_to_ignore = ['alt', 'tab', 'shift']

def on_key_event(event):
    if event.name not in keys_to_ignore:
        if event.name == 'backspace':
            print(f' {event.name} ', end='')
        elif event.name == 'space':
            print(' ', end='')
        else:
            print(event.name, end='')

keyboard.on_press(on_key_event)

# Держим программу работающей
keyboard.wait('esc')
