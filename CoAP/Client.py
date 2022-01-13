import socket
import threading
import json

import select

import CoAP.Message
import CoAP.Interface


class Client:
    received_message = None
    sent_message = None
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
        cls.sent_message = CoAP.Message.Message('Client')
        cls.received_message = CoAP.Message.Message('Server')

        cls.client_ip = CoAP.Interface.BaseWindow.client_ip
        cls.server_ip = CoAP.Interface.BaseWindow.server_ip

        cls.client_port = CoAP.Interface.BaseWindow.client_port
        cls.server_port = CoAP.Interface.BaseWindow.server_port
        cls.data = None

        cls.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        cls.client_socket.bind((cls.client_ip, cls.client_port))
        cls.client_message = CoAP.Message.Message('Client')

        cls.running = False
        cls.receive_thread = threading.Thread(target=cls.receive_fct, args=(cls.client_socket,))

    @classmethod
    def client_connect(cls):
        cls.running = True

    @classmethod
    def client_disconnect(cls):
        cls.running = False

    @classmethod
    def set_data(cls, data):
        cls.data = data

    @classmethod
    def send_to_server(cls, command, parameters, sent_message):
        try:
            cls.receive_thread = threading.Thread(target=cls.receive_fct)
            cls.receive_thread.start()
        except:
            print("Error at starting the thread!")
            return
        # while True:
        if True:
            sent_message.set_client_payload(command, parameters)
            packed_data = sent_message.encode_message()
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
        cls.received_message = CoAP.Message.Message('Server')

        header_format, encoded_json = cls.received_message.get_header_message(data)
        print(header_format, encoded_json)
        cls.received_message.decode_message(header_format, encoded_json)

        cls.sent_message = cls.received_message.verify_format()
        cls.data = cls.sent_message.encode_message()
