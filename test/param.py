import paramiko
import time
import _thread


hostname = 'w-iscdns1.ops.shbt.qihoo.net'
port = 6000
username = 'yinqiwei'
password = 'kexiaocui'
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
        time.sleep(0.5)
        command = input()
        if command == 'quitshell':
            print('Bye Bye!')
            exit(0)
        chan.send(command+'\n')
