import socket


class SocketClient:
    host = "localhost"
    port = 8000

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect((self.host, self.port))

    def close(self):
        self.sock.close()

    def recv(self) -> bytes:
        return self.sock.recv(1024)

    def send(self, msg: bytes) -> int:
        return self.sock.send(msg)
