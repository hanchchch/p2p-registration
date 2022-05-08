import os
from hashlib import sha256
from .types import EnrollMessageTypes, ProjectTypes
from .header import EnrollHeader
from .message import EnrollMessage
from .utils import utf8_with_crlf, itob


class EnrollOutgoingMessage(EnrollMessage):
    def assemble(self) -> bytes:
        raise NotImplementedError


class EnrollRegister(EnrollOutgoingMessage):
    retry_count: int = 100000000

    def __init__(
        self,
        challenge: bytes,
        team_number: int,
        project: ProjectTypes,
        email: str,
        firstname: str,
        lastname: str,
        gitlab_username: str,
    ):
        self.challenge = challenge
        self.team_number = team_number
        self.project = project
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.gitlab_username = gitlab_username

        self.payload = self.get_payload_with_pow()
        self.header = EnrollHeader.create(
            payload_size=len(self.payload), type=EnrollMessageTypes.REGISTER
        )
        self.dump()

    def get_nonce(self) -> bytes:
        return os.urandom(8)

    def get_payload(self) -> bytes:
        return (
            self.challenge
            + itob(self.team_number)
            + itob(self.project)
            + self.get_nonce()
            + utf8_with_crlf(self.email)
            + utf8_with_crlf(self.firstname)
            + utf8_with_crlf(self.lastname)
            + utf8_with_crlf(self.gitlab_username)
        )

    def get_payload_with_pow(self) -> bytes:
        for _ in range(0, self.retry_count):
            payload = self.get_payload()
            if self.validate(payload):
                return payload

        raise Exception("Failed to generate valid payload")

    def validate(self, payload: bytes) -> bool:
        return sha256(payload).hexdigest().startswith("000000")

    def assemble(self) -> bytes:
        return self.header.assemble() + self.payload
