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
    f = Fernet(crypto_key)
    # Encrypt all arguments
    encoded_args = list()
    for arg in args:
        if not isinstance(arg, bytes):
            arg = arg.encode()
        encoded_args.append(arg)
    encrypted_args = [f.encrypt(arg) for arg in encoded_args]
    # Call function with encrypted arguments
    yield aspectlib.Proceed(*encrypted_args)

@Aspect(bind=True)
def decrypt(cut_point, *args, **kws):
    """
    Decrypts the args of the given function.
    """
    f = Fernet(crypto_key)
    # Decrypt all arguments
    decrypted_args = list()
    for arg in args:
        if not isinstance(arg, bytes):
            arg = arg.decode()
        decrypted_args.append(arg)
    decrypted_args = [f.decrypt(arg) for arg in args]
    # Call function with decrypted arguments
    yield aspectlib.Proceed(*decrypted_args)




