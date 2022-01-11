import threading
import socket
import sys
import select
import json

from CoAP.Message import Message


def receive_fct(s):
    global running
    contor = 0
    while running:
        r, _, _ = select.select([s], [], [], 1)
        if not r:
            contor = contor + 1
        else:
            data, address = s.recvfrom(1024)
            print("S-a receptionat ", str(data), " de la ", address)
            print("Contor= ", contor)

@classmethod
def process_data(cls, data, address):
    # data is of type packed_data
    """
    header_format - (81, 38, 255, 255, 0, 255)
    encoded_json - b'{"command": "hello"}'
    command - hello
    """
    header_format, encoded_json = cls.Message.get_header_message(data)
    command = json.loads(encoded_json)['command']
    print(command)

    # verify header format from data and do CoAP Codes
    cls.Message.verify_message(header_format, command)


def main():
    # interfata client (butoane pentru start/stop, conn/disconn, clear screen, confirmable, exit)
    my_message = Message('Server')
    global running
    # server_socket = None


    server_port = 2001  # my port
    client_port = 2000  # peer port
    server_ip = "127.0.0.1"  # peer ip
    client_ip = "127.0.0.2"

    # Creare socket UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.bind((server_ip, int(server_port)))

    running = True
    try:
        receive_thread = threading.Thread(target=receive_fct, args=(s,))
        receive_thread.start()
    except:
        print("Eroare la pornirea thread‐ului")
        sys.exit()

    while True:
        try:
            data, address = s.recvfrom(1024)
            print("Received", str(data), "from", address)
            # process_data(data, address)
            s.sendto(b"Mesaj", (client_ip, int(client_port)))
        except KeyboardInterrupt:
            running = False
            print("Waiting for the thread to close...")
            receive_thread.join()
            break


if __name__ == '__main__':
    main()