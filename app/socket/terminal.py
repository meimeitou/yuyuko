from flask_socketio import SocketIO, Namespace
from flask import session
import logging
import pty
import os
import subprocess
import select
import termios
import struct
import fcntl
import shlex
import logging


socketio = SocketIO()
async_mode = None

session_fd = None
session_child = None

def init_terminal(app):
    global socketio
    socketio = SocketIO(app, cors_allowed_origins='*',
                        engineio_logger=True, async_mode=async_mode,
                        path="socket/terminal.io")
    socketio.on_namespace(MyNamespace('/pty'))


def set_winsize(fd, row, col, xpix=0, ypix=0):
    logging.debug("setting window size with termios")
    winsize = struct.pack("HHHH", row, col, xpix, ypix)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)


def read_and_forward_pty_output():
    max_read_bytes = 1024 * 20
    while True:
        socketio.sleep(0.01)
        if session_fd:
            timeout_sec = 0
            (data_ready, _, _) = select.select(
                [session_fd], [], [], timeout_sec)
            if data_ready:
                output = os.read(session_fd, max_read_bytes).decode()
                socketio.emit(
                    "pty-output", {"output": output}, namespace="/pty")


class MyNamespace(Namespace):
    # @socketio.on("pty-input", namespace="/pty")
    def on_ptyinput(self, data):
        """write to the child pty. The pty sees this as if you are typing in a real
        terminal.
        """
        if session_fd:
            logging.debug("received input from browser: %s" % data["input"])
            os.write(session_fd, data["input"].encode())

    # @socketio.on("resize", namespace="/pty")

    def on_resize(self, data):
        if session_fd:
            logging.debug(f"Resizing window to {data['rows']}x{data['cols']}")
            set_winsize(session_fd, data["rows"], data["cols"])

    # @socketio.on("connect", namespace="/pty")

    def on_connect(self, data):
        global session_child
        global session_fd
        """new client connected"""
        logging.info("new client connected")
        
        if "child_pid" in session:
            return

        # create child process attached to a pty we can read from and write to
        (child_pid, fd) = pty.fork()
        if child_pid == 0:
            # 子进程
            # this is the child process fork.
            # anything printed here will show up in the pty, including the output
            # of this subprocess
            subprocess.run("bash")
        else:
            # 父进程
            # this is the parent process fork.
            # store child fd and pid
            session_fd = fd
            session_child = child_pid
            set_winsize(fd, 50, 50)
            cmd = shlex.quote("bash") 
            # logging/print statements must go after this because... I have no idea why
            # but if they come before the background task never starts
            socketio.start_background_task(target=read_and_forward_pty_output)

            logging.info(f"child pid is {child_pid}")
            logging.info(
                f"starting background task with command `{cmd}` to continously read "
                "and forward pty output to client"
            )
            logging.info("task started")
