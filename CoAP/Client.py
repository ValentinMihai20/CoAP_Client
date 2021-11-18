import socket


class Client:
    def __init__(self, client_port: int, server_port: int, server_ip: str):
        self.client_port = client_port
        self.server_port = server_port
        self.server_ip = server_ip
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    def connect(self):
        self.socket.bind(self.server_ip, int(self.client_port))

