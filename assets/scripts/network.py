import contextlib
import socket
import pickle

class Network:
    def __init__(self, ip):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection = ip.split(":")
        # self.server = connection[0]
        # self.port = int(connection[1])
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()
    def get_p(self):
        return self.p

    def connect(self):
        with contextlib.suppress(Exception):
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(4096))

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(4096))
        except socket.error as e:
            print(e)
