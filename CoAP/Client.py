import socket
import threading

import select


class Client:
    client_socket = None
    ip = ""  # ip for client and server
    client_port = 0
    server_port = 0
    data = None
    running = False
    receive_thread = None

    @classmethod
    def __init__(cls):
        cls.ip = "127.0.0.1"  # local ip both client and server have
        cls.client_port = 2000  # peer port
        cls.server_port = 2001  # my port
        cls.data = None

        cls.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        cls.client_socket.bind(("127.0.0.1", cls.client_port))

        cls.running = False
        cls.receive_thread = threading.Thread(target=cls.receive_fct, args=(cls.client_socket,))

    @classmethod
    def receive_fct(cls):
        counter = 0
        while cls.running:
            # Apelam la functia sistem IO -select- pentru a verifca daca socket-ul are date in bufferul de receptie
            # Stabilim un timeout de 1 secunda
            r, _, _ = select.select([cls.client_socket], [], [], 1)
            if not r:
                counter = counter + 1
            else:
                data, address = cls.client_socket.recvfrom(1024)
                print("Received ", str(data), " from ", address)
                print("Counter = ", counter)
