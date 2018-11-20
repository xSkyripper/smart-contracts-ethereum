import aspectlib
from aspectlib import Aspect
from cryptography.fernet import Fernet


# Put this somewhere safe!
crypto_key = b'VWT2O-QQd4IIFy8qARJpSmDkB7Q3pcU0Tdbev_VTqpY='

@Aspect(bind=True)
def encrypt(cut_point, *args, **kws):  
    """
    Encrypts the arguments of the given function.
    """
    # encrypt message
    f = Fernet(crypto_key)
    encrypted_args = [f.encrypt(arg) for arg in args]
    yield aspectlib.Proceed(encrypted_args, kws)

@Aspect(bind=True)
def decrypt(cut_point, *args, **kws):
    """
    Decrypts the result of the given function.
    """
    result = yield aspectlib.Proceed
    f = Fernet(crypto_key)
    return aspectlib.Return(f.decrypt(result))



