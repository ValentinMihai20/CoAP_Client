import socket
import threading

import select

from CoAP.Message import Message

class Client:
    Message = None
    client_socket = None
    ip = ""  # ip for client and server
    client_port = 0
    server_port = 0
    data = None
    running = False
    receive_thread = None

    @classmethod
    def __init__(cls):
        cls.ip = "127.0.0.2"  # local ip both client and server have

        # adresa ip de mai sus trebuie schimbata
        # trebuie sa luam adresa ip din interfata, ca sa ne fie mai usor
        # butoane pentru fiecare actiune(more or less)

        cls.client_port = 2000  # peer port
        cls.server_port = 2001  # my port
        cls.data = None

        cls.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        cls.client_socket.bind(("127.0.0.2", cls.client_port))
        cls.client_message = Message('Client')


        cls.running = False
        cls.receive_thread = threading.Thread(target=cls.receive_fct, args=(cls.client_socket,))

    @classmethod
    def client_connect(cls):
        cls.running = True
        cls.send_to_server()

    @classmethod
    def client_disconnect(cls):
        cls.running = False

    @classmethod
    def set_data(cls, data):
        cls.data = data

    @classmethod
    def send_to_server(cls, client_message=None):
        my_message = Message('Client')
        try:
            cls.receive_thread = threading.Thread(target=cls.receive_fct)
            cls.receive_thread.start()
        except:
            print("Error at starting the thread!")
            return

        while True:
            data = input("Trimite: ")
            my_message.set_client_payload(client_message)
            packed_data = my_message.encode_message
            if data is not None:
                cls.client_socket.sendto(bytes(str(packed_data), encoding="ascii"), (cls.ip, int(cls.client_port)))
                cls.data = None
            if not cls.running:
                print("Waiting for the thread to close.")
                cls.receive_thread.join()
                print("Thread receive_thread closed.")
                break

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
