from cryptography.fernet import Fernet
import base64
import hashlib

class AESCipher:
    def __init__(self, password):
        key = hashlib.sha256(password.encode()).digest()
        self.cipher = Fernet(base64.urlsafe_b64encode(key[:32]))

    def encrypt(self, data):
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data):
        return self.cipher.decrypt(encrypted_data.encode()).decode()
