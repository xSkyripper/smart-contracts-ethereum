import hashlib

hash_object = hashlib.sha256(b'Hello World')
hex_dig = hash_object.hexdigest()

def hash256(fn):
    """
    Hashes the arguments of the given function, using sha256.
    """
    def wrapped(*args, **kws):
        retVal = fn(*args, **kws)
        # decrypt message
        return retVal
    return wrapped