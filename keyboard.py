from pynput import keyboard

keys = []

def on_press(key):
    if keys.count(key) == 0:
        keys.append(key)
    print("Pressing")
    print(keys)
    if key == keyboard.Key.esc:
        print("parando listener")
        return False

def on_release(key):
    while keys.count(key) > 0:
        keys.remove(key)


listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
listener.join()