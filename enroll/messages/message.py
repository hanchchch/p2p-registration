from .header import EnrollHeader


class EnrollMessage:
    header: EnrollHeader
    payload: bytes

    def dump(self):
        msg = self.header.assemble() + self.payload
        for i in range(0, len(msg)):
            print("{0:02x}".format(msg[i]), end=" ")
            if (i + 1) % 8 == 0:
                print()
        print()
