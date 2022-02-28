from flask_socketio import SocketIO, send, emit

socketio = SocketIO()

def init_socket(app):
    global socketio 
    socketio = SocketIO(app,cors_allowed_origins='*',engineio_logger=True)

@socketio.on('message')
def handle_message(message):
    send(message)

@socketio.on('json')
def handle_json(json):
    send(json, json=True)

@socketio.on('my event')
def handle_my_custom_event(json):
    emit('my response', json, namespace='/chat')
