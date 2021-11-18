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


