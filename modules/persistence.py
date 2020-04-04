import os.path
import winreg

#Following code was pieced together from the following StackOverFlow Post
#https://stackoverflow.com/questions/51087150/make-a-python-script-launch-itself-at-startup
#Uses registry keys


def create_key(name: str = "default", path: "" = str) -> bool:
    # initialize key (create) or open
    reg_key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Run',0, winreg.KEY_WRITE)
    if not reg_key:
        return False
    winreg.SetValueEx(reg_key, name, 0, winreg.REG_SZ, path)
    reg_key.Close()
    return True
def tryPersistence():
    #We will call this Task Manager --- Will make registry entry if successfully, otherwise return it wasnt successful
    if create_key("Task Manager for Python", str(os.path.realpath(__file__))):
        print("Added startup key.")
        return True
    else:
        print("Failed to add startup key.")
        return False


