from contrib.socket import SocketClient
from enroll.messages.outgoing import EnrollRegister
from .messages.incoming import (
    EnrollFailure,
    EnrollHeader,
    EnrollIncommingMessage,
    EnrollInit,
    EnrollSuccess,
)
from .messages.types import EnrollMessageTypes, ProjectTypes


class EnrollClient(SocketClient):
    host: str = "p2psec.net.in.tum.de"
    port: int = 13337
    incoming_msg: EnrollIncommingMessage = None

    def __init__(
        self,
        project: ProjectTypes,
        email: str,
        firstname: str,
        lastname: str,
        gitlab_username: str,
        team_number: int = 65535,
    ):
        super().__init__()
        self.team_number = team_number
        self.project = project
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.gitlab_username = gitlab_username

    def wait(self):
        msg = self.recv()
        header = EnrollHeader(msg)

        if header.type == EnrollMessageTypes.INIT:
            self.incoming_msg = EnrollInit(msg)
            return self.on_init(self.incoming_msg)

        elif header.type == EnrollMessageTypes.SUCCESS:
            self.incoming_msg = EnrollSuccess(msg)
            return self.on_success(self.incoming_msg)

        elif header.type == EnrollMessageTypes.FAILURE:
            self.incoming_msg = EnrollFailure(msg)
            return self.on_failure(self.incoming_msg)

        else:
            raise Exception("Unknown message type: " + str(header.type))

    def on_init(self, msg: EnrollInit):
        print("[Received] INIT")
        print("challenge: " + str(msg.challenge))

    def on_success(self, msg: EnrollSuccess):
        print("[Received] SUCCESS")
        print("reserved: " + str(msg.reserved))
        print("Team number: " + str(msg.team_number))

    def on_failure(self, msg: EnrollFailure):
        print("[Received] FAILURE")
        print("reserved: " + str(msg.reserved))
        print("Error number: " + str(msg.error_number))
        print("Error description: " + str(msg.error_description))

    def register(self, challenge: bytes):
        register_msg = EnrollRegister(
            challenge,
            self.team_number,
            self.project,
            self.email,
            self.firstname,
            self.lastname,
            self.gitlab_username,
        )
        sent = self.send(register_msg.assemble())
        if sent != register_msg.header.size:
            raise Exception("Failed to send message")

        print("[Sent] REGISTER")

    def run(self):
        self.connect()

        try:
            self.wait()

            if isinstance(self.incoming_msg, EnrollInit):
                self.register(self.incoming_msg.challenge)
            else:
                raise Exception("Expected INIT message")

            self.wait()

        except Exception as e:
            self.close()
            raise e

        self.close()
