import struct
from struct import *
import json


class CoAP:
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
        self.msg_class = 1
        self.msg_code = 1
        self.msg_id = 0xFFFF

        self.token = 0
        self.payload = {'command': 'Hello'}

    def verify_message(self, message):
        msg_version = (0xC0 & message[0]) >> 6
        msg_type = (0x30 & message[0]) >> 4
        msg_token_length = (0x0F & message[0]) >> 0

        msg_class = (message[1] >> 5) & 0b111
        msg_code = (message[1] >> 0) & 0x1F
        msg_id = (message[2] << 8) | message[3]

        if msg_version != CoAP.COAP_VERSION:
            print("Error")

        if 9 <= msg_token_length <= 15:
            print("Error")

        token = 0
        if msg_token_length:
            token = message[4:4 + msg_token_length]

        # payload = message[5 + msg_token_length:].decode('utf-8')

    def decode_message(self, message):
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
        message.append(0xFF & CoAP.COAP_PAYLOAD_MARKER)

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
            self.payload = {'command': command, 'data': response}

        # function for client only

    def set_client_payload(self, command):
        if self.architecture_type == 'Client':
            self.payload = {'command': command}

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

    def print_details(self):
        print("We are printing the message format...")
        print("VERSION: " + str(self.get_version()))
        print("TYPE: " + str(self.get_type()))
        print("CLASS.CODE: " + (str(self.get_class()) + "." + str(self.get_code())))
        print("MESSAGE ID: " + str(self.get_message_id()))
        print("Token: " + str(self.get_token()))
        print("Payload: " + str(self.get_payload()))

