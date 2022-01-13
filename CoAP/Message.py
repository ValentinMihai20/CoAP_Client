import struct
from struct import *
import json
import CoAP.Interface
import CoAP.Client


class CoAPFormat:
    COAP_PAYLOAD_MARKER = 0xff
    COAP_VERSION = 1

    # Message types
    TYPE_CONF = 0
    TYPE_NON_CONF = 1
    TYPE_ACK = 2
    TYPE_RESET = 3

    # Message classes
    CLASS_METHOD = 0
    CLASS_SUCCESS = 2
    CLASS_CLIENT_ERROR = 4
    CLASS_SERVER_ERROR = 5

    # Method codes
    CODE_EMPTY = 0
    CODE_GET = 1
    CODE_POST = 2
    CODE_RENAME = 8


def unpack_helper(fmt, data):
    size = struct.calcsize(fmt)
    return struct.unpack(fmt, data[:size]), data[size:]


class Message:
    def __init__(self, architecture_type):
        self.architecture_type = architecture_type
        self.msg_version = 1
        self.msg_type = 1
        self.msg_token_length = 1
        self.msg_class = 0
        self.msg_code = 1
        self.msg_id = 0xFFFF
        self.token = 0
        self.payload_marker = 0xff
        self.payload = {'command': 'Hello', 'response': 'raspuns'}

    def set_msg_version(self, msg_version):
        self.msg_version = msg_version

    def set_msg_type(self, msg_type):
        self.msg_type = msg_type

    def set_msg_token_length(self, msg_token_length):
        self.msg_token_length = msg_token_length

    def set_msg_class(self, msg_class):
        self.msg_class = msg_class

    def set_msg_code(self, msg_code):
        self.msg_code = msg_code

    def set_msg_id(self, msg_id):
        self.msg_id = msg_id

    def set_token(self, token):
        self.token = token

    def set_payload_marker(self, marker):
        self.payload_marker = marker

    def set_payload(self, payload):
        self.payload = payload

    def verify_format(self):
        if self.architecture_type == 'Server':
            response = Message('Client')

            response.set_msg_version(1)
            response.set_msg_token_length(1)
            response.set_msg_id(0xffff)
            response.set_token(0)
            response.set_payload_marker(0xff)

            # de trimis un mesaj pt ack cu confirmare de primire
            # credem ca e okay

            if self.msg_type == 0:
                #response.set_client_payload("Da, am primit mesajul","")
                response.set_msg_type(2)
                response.set_msg_class(0)
                response.set_msg_code(0)
                response.set_payload_marker(0)
                CoAP.Client.Client.send_to_server("Da, am primit mesajul", "", response)
                CoAP.Interface.BaseWindow.print_message("Da, am primit mesajul")

            if self.msg_version != 1:
                message = "Server error"  # 500 Internal Server Error

                response.set_msg_class(5)
                response.set_msg_code(0)
                response.set_msg_type(0)
                response.set_payload_marker(0)
                response.set_payload("500 Internal Server Error!")
                CoAP.Interface.BaseWindow.print_message("500 Internal Server Error!")
                return response

            if self.msg_class == 5:
                if self.msg_code == 1:
                    message = "Not implemented!"

                    response.set_msg_class(5)
                    response.set_msg_code(0)
                    response.set_msg_type(0)
                    response.set_payload_marker(0)
                    response.set_payload("501 Not implemented!")
                    CoAP.Interface.BaseWindow.print_message("501 Not implemented!")
                    return response

                if self.msg_code == 2:
                    message = "Bad Gateway!"

                    response.set_msg_class(5)
                    response.set_msg_code(0)
                    response.set_msg_type(0)
                    response.set_payload_marker(0)
                    response.set_payload("502 Bad Gateway!")
                    CoAP.Interface.BaseWindow.print_message("502 Bad Gateway!")
                    return response

                if self.msg_code == 3:
                    message = "Service Unavailable!"

                    response.set_msg_class(5)
                    response.set_msg_code(0)
                    response.set_msg_type(0)
                    response.set_payload_marker(0)
                    response.set_payload("503 Service Unavailable!")
                    CoAP.Interface.BaseWindow.print_message("503 Service Unavailable!")

                    return response

                if self.msg_code == 4:
                    message = "Gateway Timeout!"

                    response.set_msg_class(5)
                    response.set_msg_code(0)
                    response.set_msg_type(0)
                    response.set_payload_marker(0)
                    response.set_payload("504 Gateway Timeout!")
                    CoAP.Interface.BaseWindow.print_message("504 Gateway Timeout!")
                    return response

            encoded_json = self.get_payload()
            command = json.loads(encoded_json)['command']
            raspuns = json.loads(encoded_json)['response']

            print(command)
            print(raspuns)

            return response

        else:
            pass
        # creeare mesaj raspuns server pentru tip ack si non-conf?

    def decode_message(self, message, encoded_json):
        self.msg_version = (0xC0 & message[0]) >> 6
        self.msg_type = (0x30 & message[0]) >> 4
        self.msg_token_length = (0x0F & message[0]) >> 0

        self.msg_class = (message[1] >> 5) & 0b111
        self.msg_code = (message[1] >> 0) & 0x1F

        self.msg_id = (message[2] << 8) | message[3]

        self.payload_marker = (message[3])
        self.payload = encoded_json

        self.token = 0
        if self.msg_token_length:
            self.token = message[4]

        # payload = message[5 + msg_token_length:].decode('utf-8')

    def get_header_message(self, message):
        header_format, encoded_json = unpack_helper('i i i i i i ', message)
        encoded_json = encoded_json.replace(b'\x00', b'')
        return header_format, encoded_json

    def encode_message(self):
        message = [(0x03 & self.msg_version) << 6]

        message[0] |= ((self.msg_type & 0b11) << 4)
        message[0] |= (self.msg_token_length & 0x0F)

        message.append((self.msg_class & 0b11) << 5)
        message[1] |= (self.msg_code & 0x1F)

        message.append(self.msg_id >> 8)
        message.append(self.msg_id & 0xFF)

        message.append(0xFFFFFFFFFFFFFFFF & self.token)

        # urmatorul octet
        message.append(0xFF & CoAPFormat.COAP_PAYLOAD_MARKER)

        # urmatorii 0-4 octeti
        message.append(self.payload)  # message[6]

        json_message = json.dumps(message[6])
        json_size = len(json_message)
        json_message = json_message.encode()

        # prepare message to get packed
        packed_data = pack('i i i i i i ' + str(json_size) + 's',
                           message[0], message[1], message[2], message[3], message[4], message[5], json_message)

        return packed_data

        # function for server only

    def set_server_payload(self, command, response):
        if self.architecture_type == 'Server':
            self.payload = {'command': command, 'response': response}

        # function for client only

    def set_client_payload(self, command, parameters):
        if self.architecture_type == 'Client':
            self.payload = {'command': command, 'parameters': parameters}

    def get_version(self):
        return int(str(self.msg_version), 2)

    def get_type(self):
        return self.msg_type  # int(str(self.msg_type))

    def get_class(self):
        return int(str(self.msg_class))

    def get_code(self):
        return self.msg_code

    def get_message_id(self):
        return int(str(self.msg_id))

    def get_token(self):
        return int(str(self.token))

    def get_payload(self):
        return self.payload


