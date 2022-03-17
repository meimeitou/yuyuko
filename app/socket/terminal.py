from flask_socketio import SocketIO, Namespace, disconnect,ConnectionRefusedError
from flask import request
import logging
from threading import Lock
from app.socket.ssh import SSHClient
from app.socket.worker import clients, Worker
import weakref
import paramiko

thread = None
thread_lock = Lock()
socketio = SocketIO()
async_mode = "gevent"
# sshClient = None
BUF_SIZE = 32 * 1024
MAX_WORKERS = 10

def init_term(app):
    global socketio
    socketio = SocketIO(app, cors_allowed_origins='*',ping_timeout=5, ping_interval=5,
                        engineio_logger=False, async_mode=async_mode,async_handlers=True,
                        path="socket/terminal.io")
    socketio.on_namespace(MyNamespace('/pty'))


def recvThread(worker=None):
    # global sshClient
    while True:
        socketio.sleep(0.01)
        if worker:
            while worker.sshClient.chan.recv_ready():
                info = worker.sshClient.chan.recv(BUF_SIZE).decode('utf-8')
                socketio.emit(
                    "pty-output", {"output": info},
                    namespace="/pty",
                    room=worker.sid)
class MyNamespace(Namespace):
    def on_disconnect(self):
        print('Client disconnected', request.sid)
        worker = self._get_worker()
        if worker:
            worker().close()
    # 断开连接
    def on_disconnect_request(self):
        logging.info(f"on_disconnect_request request sid: {request.sid}")
        # global sshClient
        socketio.emit("pty-output", {"output": "exit\r\n"}, namespace="/pty",room=request.sid)
        disconnect()
        worker = self._get_worker()
        if worker:
            worker().close()
        # sshClient = None

    # web终端输入
    def on_ptyinput(self, data):
        # global sshClient
        worker = self._get_worker()
        logging.info(f"on_ptyinput request sid: {request.sid}")
        if worker:
            # logging.info("received input from browser: %s" % repr(data["input"].encode()))
            worker().sshClient.send(data["input"].encode())
            if data["input"].encode() == b'\x04':
                socketio.emit(
                    "pty-output", {"output": "exit\r\n"},
                    namespace="/pty", room=request.sid)
                disconnect()
                worker().close()

    # 终端调整大小
    def on_resize(self, data):
        # global sshClient
        worker = self._get_worker()
        if worker:
            logging.debug(f"Resizing window to {data['rows']}x{data['cols']}")
            worker().sshClient.resize_window(data["cols"], data["rows"])

    # 连接ssh
    def on_ssh(self, data):
        logging.info(f"connecting ssh...,{data}")
        ip = self._get_remote_ip()
        sid = request.sid
        if self._get_worker() is not None:
            logging.info("already connected...")
            return
        
        if ip in clients:
            if len(clients.get(ip))>=MAX_WORKERS:
                logging.info("client max connection reached...")
                socketio.emit(
                    "pty-output", {"output": "client max connection reached..\r\n"},
                    namespace="/pty",room=sid)
                disconnect()
                return
        logging.info("new client connected")
        try:
            
            sshClient = SSHClient(host=data["host"], port=data["port"],
                                user=data["user"], password=data["password"])
            sshClient.resize_window(data["cols"], data["rows"])
            worker = Worker(ip, sid, sshClient)
        except Exception as e:
            socketio.emit(
                    "pty-output", {"output": "连接失败...\r\n"},
                    namespace="/pty",room=sid)
            socketio.emit(
                    "pty-output", {"output": f"{e}\r\n"},
                    namespace="/pty",room=sid)
            disconnect()
            return
        if ip in clients:
            clients[ip][sid] = worker
        else:
            clients[ip] = {}
            clients[ip][sid] = worker
        global thread
        with thread_lock:
            if thread is None:
                socketio.start_background_task(target=recvThread, worker=worker)

    # 连接
    def on_connect(self):
        logging.info(f'client ip: {self._get_remote_ip()} sid: {request.sid}, connected...')
    # create or old
    def _get_worker(self):
        ip = self._get_remote_ip()
        sid = request.sid
        if ip in clients:
            if sid in clients.get(ip):
                return weakref.ref(clients.get(ip).get(sid))
        return None

    def _get_remote_ip(self):
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            return request.environ['REMOTE_ADDR']
        else:
            request.environ['HTTP_X_FORWARDED_FOR']
