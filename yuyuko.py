from time import sleep
from app import app, cli
import webbrowser
from threading import Timer
from app.socket.socket import socketio


cli.register(app)

def open_browser():
    webbrowser.open('http://127.0.0.1:5577/')

if __name__ == '__main__':
    # Timer(1, open_browser).start()
    # app.run("0.0.0.0", 5588)
    socketio.run(app, "0.0.0.0", 5588)
