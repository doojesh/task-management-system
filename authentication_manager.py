import bcrypt
import pyotp

class AuthMgr:
    def __init__(self):
        self.secret = pyotp.random_base32()

    def generate_otp(self):
        totp = pyotp.TOTP(self.secret)
        return totp.now()

    def verify_otp(self, otp):
        totp = pyotp.TOTP(self.secret)
        return totp.verify(otp)

    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()

    @staticmethod
    def verify_password(password, hashed_password):
        return bcrypt.checkpw(password.encode(), hashed_password.encode())