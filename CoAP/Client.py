import socket
import threading

import select

from CoAP.Message import Message


class Client:
    '''
    sent_message = Message('Client')
    client_port = 2000
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    client_socket.bind(("127.0.0.2", client_port))
    '''
    received_message = None
    client_socket = None
    client_ip = ""
    server_ip = ""
    client_port = 0
    server_port = 0
    data = None
    running = False
    receive_thread = None

    @classmethod
    def __init__(cls):
        cls.sent_message = Message('Client')
        cls.received_message = Message('Server')
        cls.client_ip = "127.0.0.2"  # local ip both client and server have
        cls.server_ip = "127.0.0.1"
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
        #cls.send_to_server()


    @classmethod
    def client_disconnect(cls):
        cls.running = False

    @classmethod
    def set_data(cls, data):
        cls.data = data

    @classmethod
    def send_to_server(cls, command, parameters):
        try:
            cls.receive_thread = threading.Thread(target=cls.receive_fct)
            cls.receive_thread.start()
        except:
            print("Error at starting the thread!")
            return

        if True:
            command = command
            parameters = parameters
            cls.sent_message.set_client_payload(command, parameters)
            packed_data = cls.sent_message.encode_message()
            if command is not None:
                cls.client_socket.sendto(packed_data, (cls.server_ip, int(cls.server_port)))
                cls.data = None
            if not cls.running:
                print("Waiting for the thread to close.")
                cls.receive_thread.join()
                print("Thread receive_thread closed.")
               # break

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
                cls.process_data(data)
                print(data)


    @classmethod
    def process_data(cls, data):
        header_format, encoded_json = cls.received_message.get_header_message(data)

        cls.received_message.decode_message(header_format, encoded_json)
        # cls.sent_message.verify din message.py
        cls.sent_message = cls.received_message.verify_format()
        cls.data = cls.sent_message.encode_message()
