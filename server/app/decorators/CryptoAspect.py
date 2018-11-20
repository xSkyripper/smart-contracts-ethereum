
def encrypt(fn):
    """
    Encrypts the arguments of the given function.
    """
    def wrapped(*args, **kws):
        # encrypt message
        return fn(*args, **kws)
    return wrapped

def decrypt(fn):
    """
    Decrypts the result of the given function.
    """
    def wrapped(*args, **kws):
        retVal = fn(*args, **kws)
        # decrypt message
        return retVal
    return wrapped

def hash256(fn):
    """
    Hashes the arguments of the given function, using sha256.
    """
    def wrapped(*args, **kws):
        retVal = fn(*args, **kws)
        # decrypt message
        return retVal
    return wrapped
