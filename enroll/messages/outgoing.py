import os
from hashlib import sha256
from multiprocessing import Pool

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

        self.payload = self.get_payload()
        self.header = EnrollHeader.create(
            payload_size=len(self.payload), type=EnrollMessageTypes.REGISTER
        )
        self.dump()

    def get_payload_a(self) -> bytes:
        return self.challenge + itob(self.team_number) + itob(self.project)

    def get_payload_b(self) -> bytes:
        return (
            utf8_with_crlf(self.email)
            + utf8_with_crlf(self.firstname)
            + utf8_with_crlf(self.lastname)
            + utf8_with_crlf(self.gitlab_username)
        )

    @staticmethod
    def proof_of_work(args: list) -> bytes:
        payload_a, payload_b, retry_count = args
        for _ in range(retry_count):
            nonce = os.urandom(8)
            payload = payload_a + nonce + payload_b
            if sha256(payload).hexdigest().startswith("000000"):
                return nonce

    def get_nonce(self) -> bytes:
        pool_count = 4

        pool = Pool(pool_count)
        nonces = pool.imap_unordered(
            EnrollRegister.proof_of_work,
            [
                [
                    self.get_payload_a(),
                    self.get_payload_b(),
                    self.retry_count // pool_count,
                ]
                for _ in range(0, pool_count)
            ],
        )

        pool.close()
        for valid_nonce in nonces:
            if valid_nonce:
                pool.terminate()
                return valid_nonce
        pool.join()

        raise Exception("Failed to generate valid payload")

    def get_payload(self) -> bytes:
        return self.get_payload_a() + self.get_nonce() + self.get_payload_b()

    def assemble(self) -> bytes:
        return self.header.assemble() + self.payload
