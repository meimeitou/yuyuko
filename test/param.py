import paramiko
import time
import _thread


hostname = 'localhost'
port = 22
username = ''
password = ''
timeout = 10

def recvThread():  # 开启一个多线程负责读取返回信息
    global chan
    while True:
        while chan.recv_ready():
            info = chan.recv(1024).decode('utf-8')
            print(info, end='')
            time.sleep(0.1)

if __name__ == "__main__":
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)
    chan = ssh.invoke_shell()  # 创建一个交互式的shell窗口
    chan.settimeout(1000)
    _thread.start_new_thread(recvThread, ())

    while True:
        if chan.closed:
            exit(0)
        time.sleep(0.5)
        command = input()
        if command == 'quitshell':
            print('Bye Bye!')
            chan.send(chr(3))
            chan.close()
            break
        chan.send(command+'\n')
