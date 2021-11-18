class CoAP:
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


class Message:
    def __init__(self, payload: str, msg_type: int, msg_class: int, msg_code: int, msg_id: int, msg_token_length: int,
                 msg_version=1, token=0):
        self.msg_version = msg_version
        self.msg_type = msg_type
        self.msg_token_length = msg_token_length
        self.msg_class = msg_class
        self.msg_code = msg_code
        self.msg_id = msg_id

        self.token = token
        self.payload = payload

    @classmethod
    def decode_message(cls, message: bytes):
        msg_version = (0xC0 & message[0]) >> 6
        msg_type = (0x30 & message[0]) >> 4
        msg_token_length = (0x0F & message[0]) >> 0
        msg_class = (message[1] >> 5) & 0b111
        msg_code = (message[1] >> 0) & 0x1F
        msg_id = (message[2] << 8) | message[3]

        if msg_version != 1:
            print("Error")

        if 9 <= msg_token_length <= 15:
            print("Error")

        token = 0
        if msg_token_length:
            token = message[4:4 + msg_token_length]

        payload = message[5 + msg_token_length:].decode('utf-8')
        return cls(payload, msg_type, msg_class, msg_code, msg_id, msg_token_length, msg_version=1, token=0)

    def encode_message(self):
        message = [(0x03 & self.msg_version) << 6]

        message[0] |= ((self.msg_type & 0b11) << 4)
        message[0] |= (self.msg_token_length & 0x0F)

        message.append((self.msg_class & 0b11) << 5)
        message[1] |= (self.msg_code & 0x1F)

        message.append(self.msg_id >> 8)
        message.append(self.msg_id & 0xFF)

        if self.msg_token_length:
            message = (message << 8 * self.msg_token_length) | self.token

        if len(self.payload):
            self.payload.encode('utf-8')
        for i in range(0, len(self.payload)):
            message.append(self.payload[i])

        return message.to_bytes(message + self.msg_token_length, 'big')

