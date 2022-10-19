from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken


class Cryptor:

    def __init__(self, keyfile: str) -> None:
        self.keyfile = keyfile
        try:
            with open(self.keyfile, 'rb') as file:
                self.key = file.read()
        except FileNotFoundError:
            self.key = Fernet.generate_key()
            with open(self.keyfile, 'wb') as file:
                file.write(self.key)
            print('Key generated')
        self.fernet = Fernet(self.key)

    def encrypt(self, msg: bytes) -> bytes:
        # return msg
        return self.fernet.encrypt(msg)

    def decrypt(self, encrypted_msg: bytes) -> bytes:
        # return encrypted_msg
        try:
            return self.fernet.decrypt(encrypted_msg)
        except InvalidToken:
            return b'Unknown message key! Please verify your AES key-file.'

