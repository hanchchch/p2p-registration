from enroll.messages.utils import btoi
from .header import EnrollHeader
from .message import EnrollMessage


class EnrollIncommingMessage(EnrollMessage):
    def __init__(self, msg: bytes):
        self.header = EnrollHeader(msg[:4])
        self.payload = msg[4:]


class EnrollInit(EnrollIncommingMessage):
    def __init__(self, msg: bytes):
        super().__init__(msg)
        self.challenge = self.payload[:8]


class EnrollSuccess(EnrollIncommingMessage):
    def __init__(self, msg: bytes):
        super().__init__(msg)
        self.reserved = btoi(self.payload[:2])
        self.team_number = btoi(self.payload[2:4])


class EnrollFailure(EnrollIncommingMessage):
    def __init__(self, msg: bytes):
        super().__init__(msg)
        self.reserved = btoi(self.payload[:2])
        self.error_number = btoi(self.payload[2:4])
        self.error_description = self.payload[4:].decode()
