import paramiko
import time
import struct

class SSHClient(object):
    def __init__(self, host, port, user, password, timeout=15) -> None:
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._timeout = timeout
        self.ssh = None
        self.chan = None
        self._init_chan()

    def _init_chan(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self._host, self._port, self._user, self._password)
        chan = self.ssh.invoke_shell(term='xterm')  # 创建一个交互式的shell窗口
        chan.settimeout(self._timeout)
        self.chan = chan

    def resize_window(self, width, height):
        try:
            # logging.info(f'{width}*{height}')
            self.chan.resize_pty(width, height)
        except (TypeError, struct.error, paramiko.SSHException):
            pass

    def send(self, command):
        self.chan.send(command)

    def recvThread(self):
        while True:
            while self.chan.recv_ready():
                info = self.chan.recv(1024*10).decode('utf-8')
                print(info, end='')
                time.sleep(0.05)
