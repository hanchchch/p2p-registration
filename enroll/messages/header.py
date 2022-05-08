from .utils import btoi, itob

HEADER_SIZE = 4


class EnrollHeader:
    def __init__(self, msg: bytes):
        self.size = btoi(msg[:2])
        self.type = btoi(msg[2:4])

    @staticmethod
    def create(payload_size: int, type: int):
        return EnrollHeader(itob(payload_size + HEADER_SIZE) + itob(type))

    def assemble(self) -> bytes:
        return itob(self.size) + itob(self.type)
