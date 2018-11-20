import aspectlib
from cryptography.fernet import Fernet


# Put this somewhere safe!
crypto_key = b'VWT2O-QQd4IIFy8qARJpSmDkB7Q3pcU0Tdbev_VTqpY='

def encrypt(fn):
    """
    Encrypts the arguments of the given function.
    """
    def wrapped(*args, **kws):
        # encrypt message
        f = Fernet(crypto_key)
        encrypted_args = [f.encrypt(arg) for arg in args]
        yield aspectlib.Proceed(encrypted_args, kws)
    return wrapped

def decrypt(fn):
    """
    Decrypts the result of the given function.
    """
    def wrapped(*args, **kws):
        result = yield aspectlib.Proceed
        f = Fernet(crypto_key)
        return aspectlib.Return(f.decrypt(result))
    return wrapped



