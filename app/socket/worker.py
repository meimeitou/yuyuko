from app.socket.ssh import SSHClient
import logging

clients = {}  # save workers, {ip: {sid: worker}}

class Worker(object):
    def __init__(self,ip:str,sid:str, client: SSHClient) -> None:
        self.sshClient = client
        self.ip = ip
        self.sid = sid
        self.closed = False
    
    def __str__(self) -> str:
        return f'{self.ip},{self.sid}'

    def close(self, reason=None):
        if self.closed:
            return
        self.closed = True

        logging.info(
            'Closing worker {} with reason: {}'.format(self.ip, reason)
        )
        self.sshClient.chan.close()
        self.sshClient.ssh.close()
        logging.info('Connection to {}:{} lost'.format(self.ip, self.sid))
        global clients
        clear_worker(self, clients)
        logging.debug(clients)

def clear_worker(worker: Worker, clients):
    workers = clients.get(worker.ip)
    assert worker.sid in workers
    workers.pop(worker.sid)

    if not workers:
        clients.pop(worker.ip)
        if not clients:
            clients.clear()
