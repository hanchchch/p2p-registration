def btoi(msg: bytes):
    return int.from_bytes(msg, byteorder="big")


def itob(num: int):
    return num.to_bytes(2, byteorder="big")


def utf8_with_crlf(msg: str):
    return f"{msg}\r\n".encode("utf-8")
